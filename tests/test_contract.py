from pathlib import Path
import ast
s=(Path(__file__).parents[1]/'contracts/contract.py').read_text()
def test_parse():ast.parse(s)
def test_briefing_lifecycle():assert all(('def '+x) in s for x in ('collect_briefing','synthesize_briefing','publish_briefing','archive_briefing','get_briefing'))
def test_records_attributable():assert "mine['digests']==theirs.get('digests')" in s and 'a[0]==b[0]' in s
