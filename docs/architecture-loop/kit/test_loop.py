"""Risk-focused regression checks. Run: python3 -m unittest -v test_loop.py"""
import contextlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from gates import ArtifactStore, GateEngine
from loop import main

KIT = Path(__file__).resolve().parent


class LoopTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "run"
        shutil.copytree(KIT / "example" / "run", self.root, ignore=shutil.ignore_patterns("snapshots", "__pycache__"))
        (self.root / "snapshots").mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def change(self, name, fn):
        p=self.root/name; data=json.loads(p.read_text());fn(data)
        p.write_text(json.dumps(data,indent=2)+'\n')

    def codes(self, stage):
        return {f.code for f in GateEngine(self.root).check(stage)}

    def command(self, *args):
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            return main(list(args))

    def good_review(self):
        data=json.loads((KIT/'templates/review.json').read_text())
        data.update(source_fingerprint=ArtifactStore(self.root).fingerprint(),reviewer='Test fixture',mode='single_model')
        for row in data['checks'].values():row.update({'pass':True,'evidence':'Synthetic unit-test declaration; not a substantive review.'})
        for row in data['scores'].values():row.update(score=3,evidence='Synthetic unit-test declaration.')
        (self.root/'review.json').write_text(json.dumps(data))

    def test_complete_example_passes_draft_structure(self):
        self.assertEqual([],GateEngine(self.root).check('draft'))

    def test_unread_source_blocks_fact(self):
        self.change('evidence.json',lambda d:d['sources'][0].update(retrieved=False))
        self.assertIn('unread_source',self.codes('research'))

    def test_missing_support_blocks_fact(self):
        self.change('evidence.json',lambda d:d['claims'][0].update(source_ids=[]))
        self.assertIn('unsupported_fact',self.codes('research'))

    def test_malformed_json_returns_finding(self):
        (self.root/'evidence.json').write_text('{broken')
        self.assertIn('invalid_artifact',self.codes('research'))

    def test_missing_code_view_is_rejected(self):
        self.change('architecture.json',lambda d:d['views'].pop())
        self.assertIn('c4_levels',self.codes('design'))

    def test_invalid_parent_is_rejected(self):
        self.change('architecture.json',lambda d:next(e for e in d['elements'] if e['id']=='Gates').update(parent='Loop'))
        self.assertIn('c4_parent',self.codes('design'))

    def test_zoom_parent_must_be_visible(self):
        self.change('architecture.json',lambda d:d['views'][1]['nodes'].remove('Runner'))
        self.assertIn('c4_continuity',self.codes('design'))

    def test_changed_model_stales_diagrams(self):
        self.change('architecture.json',lambda d:d['elements'][1].update(name='Changed system'))
        self.assertIn('stale_diagram',self.codes('design'))

    def test_orphan_slide_is_rejected(self):
        self.change('slides.json',lambda d:d['slides'].append(dict(d['slides'][0],id='P99')))
        self.assertIn('unmapped_slide',self.codes('draft'))

    def test_slide_section_claim_mismatch_is_rejected(self):
        self.change('slides.json',lambda d:d['slides'][0].update(paper_section='references'))
        self.assertIn('story_slide_mismatch',self.codes('draft'))

    def test_changed_paper_stales_review(self):
        self.good_review()
        self.assertNotIn('stale_review',self.codes('review'))
        with (self.root/'paper.md').open('a') as out:out.write('\nChanged after review.\n')
        self.assertIn('stale_review',self.codes('review'))

    def test_missing_export_is_rejected(self):
        self.good_review()
        self.change('export.json',lambda d:d.update(source_fingerprint=ArtifactStore(self.root).fingerprint(),files=[]))
        self.assertIn('required_outputs',self.codes('export'))

    def test_path_escape_is_rejected(self):
        with self.assertRaises(ValueError):ArtifactStore(self.root).path('../outside.json')

    def test_failed_gate_cannot_advance(self):
        self.change('state.json',lambda d:d.update(stage='frame',status='running'))
        self.change('brief.json',lambda d:d.update(topic=''))
        self.assertEqual(1,self.command('advance',str(self.root)))
        self.assertEqual('frame',json.loads((self.root/'state.json').read_text())['stage'])

    def test_revision_cannot_jump_forward(self):
        self.change('state.json',lambda d:d.update(stage='frame',status='running'))
        self.assertEqual(2,self.command('revise',str(self.root),'--to','export','--reason','Attempt to skip work'))

    def test_revision_budget_blocks_without_erasing_snapshot(self):
        self.change('state.json',lambda d:d.update(stage='draft',status='running',revision=0,max_revisions=1))
        self.assertEqual(0,self.command('revise',str(self.root),'--to','research','--reason','Source correction'))
        self.assertTrue((self.root/'snapshots/revision-00/paper.md').exists())
        self.assertEqual(2,self.command('revise',str(self.root),'--to','frame','--reason','Second revision'))
        state=json.loads((self.root/'state.json').read_text())
        self.assertEqual('blocked',state['status'])

    def test_prompt_budget_stops_issuing_work(self):
        self.change('state.json',lambda d:d.update(stage='frame',status='running',prompts_issued=1,max_prompts=1))
        self.assertEqual(2,self.command('prompt',str(self.root)))
        self.assertEqual('blocked',json.loads((self.root/'state.json').read_text())['status'])


if __name__=='__main__':unittest.main()
