from __future__ import annotations
import json, os, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]; DIST=ROOT/'tools/cpt_dist.py'

def run_tool(repo,*args,check=True):
    r=subprocess.run([sys.executable,str(repo/'.cpt/bin/cpt_runtime.py'),*args],cwd=repo,text=True,capture_output=True)
    if check and r.returncode!=0: raise AssertionError(f"{args}\nOUT={r.stdout}\nERR={r.stderr}")
    return r

def install(repo,home):
    env=os.environ.copy(); env['HOME']=str(home); env['CODEX_HOME']=str(home/'.codex')
    r=subprocess.run([sys.executable,str(DIST),'install','--project',str(repo),'--mode','local','--plugin-scope','none'],text=True,capture_output=True,env=env)
    if r.returncode: raise AssertionError(r.stderr)

class KnowledgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_tmp=Path(tempfile.mkdtemp(prefix='cpt-alpha7-knowledge-base-'))
        cls.base_repo=cls.base_tmp/'repo'; cls.base_repo.mkdir()
        subprocess.run(['git','init','-q',str(cls.base_repo)],check=True)
        home=cls.base_tmp/'home'; home.mkdir(); install(cls.base_repo,home)
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.base_tmp)
    def setUp(self):
        self.tmp=Path(tempfile.mkdtemp(prefix='cpt-alpha7-knowledge-case-'))
        self.repo=self.tmp/'repo'; shutil.copytree(self.base_repo,self.repo)
    def tearDown(self): shutil.rmtree(self.tmp)
    def init_kb(self,mode='existing'):
        run_tool(self.repo,'knowledge-init','--title','Test Knowledge','--mode',mode,'--owner-role','product_strategist','--source-kind','git_commit','--source-value','abc123')
    def test_existing_create_claim_render_validate(self):
        self.init_kb(); run_tool(self.repo,'knowledge-create','--id','product-map','--type','product_map','--title','Product Map','--owner-role','product_strategist','--review-path','src/**')
        run_tool(self.repo,'knowledge-claim-add','--artifact','product-map','--statement','A primary area exists.','--lifecycle','confirmed','--confidence','medium','--owner-role','product_strategist','--evidence-type','source_file','--evidence-source','src/app.ts')
        self.assertIn('KNOWLEDGE VALIDATION PASSED',run_tool(self.repo,'knowledge-validate').stdout)
        self.assertTrue((self.repo/'.cpt/knowledge/views/product-map.md').exists())
    def test_greenfield_planned_claim(self):
        self.init_kb('greenfield'); run_tool(self.repo,'knowledge-create','--id','product-map','--type','product_map','--title','Planned Map','--owner-role','product_strategist')
        run_tool(self.repo,'knowledge-claim-add','--artifact','product-map','--statement','The MVP has one core flow.','--lifecycle','planned','--confidence','medium','--owner-role','product_strategist','--evidence-type','user_approved_decision','--evidence-source','approved brief')
        self.assertEqual(run_tool(self.repo,'knowledge-validate').returncode,0)
    def test_validated_requires_test_or_observation(self):
        self.init_kb(); run_tool(self.repo,'knowledge-create','--id','area-x','--type','area_map','--title','Area','--owner-role','product_designer')
        r=run_tool(self.repo,'knowledge-claim-add','--artifact','area-x','--statement','Behavior works.','--lifecycle','validated','--confidence','high','--owner-role','qa_engineer','--evidence-type','source_file','--evidence-source','src/x.ts',check=False)
        self.assertNotEqual(r.returncode,0); self.assertIn('validated claim requires',r.stderr)
    def test_transition_rules(self):
        self.init_kb(); run_tool(self.repo,'knowledge-create','--id','decision-x','--type','decision_record','--title','Decision','--owner-role','product_strategist')
        cid=run_tool(self.repo,'knowledge-claim-add','--artifact','decision-x','--statement','Option A is preferred.','--lifecycle','hypothesized','--confidence','low','--owner-role','product_strategist').stdout.strip()
        run_tool(self.repo,'knowledge-claim-transition','--artifact','decision-x','--claim',cid,'--to','inferred','--confidence','medium')
        r=run_tool(self.repo,'knowledge-claim-transition','--artifact','decision-x','--claim',cid,'--to','planned',check=False); self.assertNotEqual(r.returncode,0)
    def test_stale_scan_and_dependency_propagation(self):
        self.init_kb(); run_tool(self.repo,'knowledge-create','--id','area-a','--type','area_map','--title','Area A','--owner-role','product_designer','--review-path','src/a/**')
        run_tool(self.repo,'knowledge-create','--id','product-map','--type','product_map','--title','Product Map','--owner-role','product_strategist','--depends-on','area-a')
        data=json.loads(run_tool(self.repo,'knowledge-stale-scan','--changed','src/a/file.ts').stdout)
        self.assertEqual(set(data['marked_artifacts']),{'area-a','product-map'})
    def test_soft_size_warning_never_truncates(self):
        self.init_kb(); run_tool(self.repo,'knowledge-create','--id','product-map','--type','product_map','--title','Product Map','--owner-role','product_strategist')
        path=self.repo/'.cpt/knowledge/artifacts/product-map.yaml'; import yaml
        d=yaml.safe_load(path.read_text()); d['content']['shared_boundaries']=[f'Boundary {i}' for i in range(300)]; path.write_text(yaml.safe_dump(d,sort_keys=False))
        run_tool(self.repo,'knowledge-render','--all'); r=run_tool(self.repo,'knowledge-validate'); self.assertEqual(r.returncode,0); self.assertIn('target guidance',r.stdout); self.assertIn('Boundary 299',(self.repo/'.cpt/knowledge/views/product-map.md').read_text())
    def test_task_completion_requires_knowledge_accounting(self):
        task=run_tool(self.repo,'create-task','--title','Task','--objective','Do work','--activate').stdout.strip()
        r=run_tool(self.repo,'complete-task',check=False); self.assertNotEqual(r.returncode,0)
        run_tool(self.repo,'knowledge-task-assess','--task',task,'--status','not_required','--summary','No durable knowledge changed.')
        run_tool(self.repo,'complete-task')
    def test_context_packet(self):
        self.init_kb(); run_tool(self.repo,'knowledge-create','--id','area-a','--type','area_map','--title','Area A','--owner-role','product_designer')
        task=run_tool(self.repo,'create-task','--title','Task','--objective','Use knowledge','--activate').stdout.strip()
        run_tool(self.repo,'knowledge-packet-create','--id','context-task','--title','Task Context','--task',task,'--artifact','area-a','--owner-role','intake_orchestrator')
        self.assertTrue((self.repo/'.cpt/knowledge/artifacts/context-task.yaml').exists())
    def test_redesign_mode_perspective(self):
        self.init_kb('redesign'); run_tool(self.repo,'knowledge-create','--id','decision-redesign','--type','decision_record','--title','Redesign Decision','--owner-role','product_designer')
        import yaml; d=yaml.safe_load((self.repo/'.cpt/knowledge/artifacts/decision-redesign.yaml').read_text()); self.assertEqual(d['perspective'],'delta')

    def test_secret_pattern_is_blocked(self):
        self.init_kb(); run_tool(self.repo,'knowledge-create','--id','area-secret','--type','area_map','--title','Area','--owner-role','product_designer')
        r=run_tool(self.repo,'knowledge-claim-add','--artifact','area-secret','--statement','Credential sk-abcdefghijklmnopqrstuvwxyz1234567890 is present.','--lifecycle','hypothesized','--confidence','low','--owner-role','product_designer',check=False)
        self.assertNotEqual(r.returncode,0); self.assertIn('possible sensitive value',r.stderr)

    def test_external_sharing_requires_policy_and_sanitization(self):
        self.init_kb(); run_tool(self.repo,'knowledge-create','--id','public-map','--type','product_map','--title','Public Map','--owner-role','product_strategist','--classification','public','--external-sharing','allowed')
        run_tool(self.repo,'knowledge-sharing-set','--artifact','public-map','--sanitization-status','not_required','--note','No sensitive material.')
        self.assertEqual(run_tool(self.repo,'knowledge-sanitize-check','--artifact','public-map','--external').returncode,0)
        run_tool(self.repo,'knowledge-create','--id','internal-map','--type','product_map','--title','Internal Map','--owner-role','product_strategist')
        r=run_tool(self.repo,'knowledge-sanitize-check','--artifact','internal-map','--external',check=False)
        self.assertNotEqual(r.returncode,0); self.assertIn('external sharing is prohibited',r.stdout)

    def test_context_packet_defaults_to_internal_prohibited(self):
        self.init_kb(); run_tool(self.repo,'knowledge-create','--id','area-a','--type','area_map','--title','Area A','--owner-role','product_designer')
        task=run_tool(self.repo,'create-task','--title','Task','--objective','Use knowledge','--activate').stdout.strip()
        run_tool(self.repo,'knowledge-packet-create','--id','context-safe','--title','Task Context','--task',task,'--artifact','area-a','--owner-role','intake_orchestrator')
        data=yaml.safe_load((self.repo/'.cpt/knowledge/artifacts/context-safe.yaml').read_text())
        self.assertEqual(data['data_classification'],'internal'); self.assertEqual(data['sharing']['external_sharing'],'prohibited')

    def test_dependency_cycle_is_rejected(self):
        self.init_kb(); run_tool(self.repo,'knowledge-create','--id','area-a','--type','area_map','--title','Area A','--owner-role','product_designer')
        run_tool(self.repo,'knowledge-create','--id','area-b','--type','area_map','--title','Area B','--owner-role','product_designer','--depends-on','area-a')
        run_tool(self.repo,'knowledge-link','--artifact','area-a','--depends-on','area-b')
        r=run_tool(self.repo,'knowledge-validate',check=False)
        self.assertNotEqual(r.returncode,0); self.assertIn('dependency cycle',r.stdout)

if __name__=='__main__': unittest.main()
