
while : ;
do
	if [[ ! -f log ]]
	then
		START_INDEX="0"
	else
		START_INDEX=`cat log | grep -E "Results [0-9]+" | tail -1 | cut -d" " -f2`
	fi
	
	echo "Current start index is ${START_INDEX}"

	python fetch_papers.py --search-query "cat:astro-ph+OR+cat:astro-ph.CO+OR+cat:astro-ph.EP+OR+cat:astro-ph.GA+OR+cat:astro-ph.HE+OR+cat:astro-ph.IM+OR+cat:astro-ph.SR+OR+cat:cond-mat.dis-nn+OR+cat:cond-mat.mes-hall+OR+cat:cond-mat.mtrl-sci+OR+cat:cond-mat.other+OR+cat:cond-mat.quant-gas+OR+cat:cond-mat.soft+OR+cat:cond-mat.stat-mech+OR+cat:cond-mat.str-el+OR+cat:cond-mat.supr-con+OR+cat:cs.AI+OR+cat:cs.AR+OR+cat:cs.CC+OR+cat:cs.CE+OR+cat:cs.CG+OR+cat:cs.CL+OR+cat:cs.CR+OR+cat:cs.CV+OR+cat:cs.CY+OR+cat:cs.DB+OR+cat:cs.DC+OR+cat:cs.DL+OR+cat:cs.DM+OR+cat:cs.DS+OR+cat:cs.ET+OR+cat:cs.FL+OR+cat:cs.GL+OR+cat:cs.GR+OR+cat:cs.GT+OR+cat:cs.HC+OR+cat:cs.IR+OR+cat:cs.IT+OR+cat:cs.LG+OR+cat:cs.LO+OR+cat:cs.MA+OR+cat:cs.MM+OR+cat:cs.MS+OR+cat:cs.NA+OR+cat:cs.NE+OR+cat:cs.NI+OR+cat:cs.OH+OR+cat:cs.OS+OR+cat:cs.PF+OR+cat:cs.PL+OR+cat:cs.RO+OR+cat:cs.SC+OR+cat:cs.SD+OR+cat:cs.SE+OR+cat:cs.SI+OR+cat:cs.SY+OR+cat:econ.EM+OR+cat:eess.AS+OR+cat:eess.IV+OR+cat:eess.SP+OR+cat:gr-qc+OR+cat:hep-ex+OR+cat:hep-lat+OR+cat:hep-ph+OR+cat:hep-th+OR+cat:math.AC+OR+cat:math.AG+OR+cat:math.AP+OR+cat:math.AT+OR+cat:math.CA+OR+cat:math.CO+OR+cat:math.CT+OR+cat:math.CV+OR+cat:math.DG+OR+cat:math.DS+OR+cat:math.FA+OR+cat:math.GM+OR+cat:math.GN+OR+cat:math.GR+OR+cat:math.GT+OR+cat:math.HO+OR+cat:math.IT+OR+cat:math.KT+OR+cat:math.LO+OR+cat:math.MG+OR+cat:math.MP+OR+cat:math.NA+OR+cat:math.NT+OR+cat:math.OA+OR+cat:math.OC+OR+cat:math.PR+OR+cat:math.QA+OR+cat:math.RA+OR+cat:math.RT+OR+cat:math.SG+OR+cat:math.SP+OR+cat:math.ST+OR+cat:math-ph+OR+cat:nlin.AO+OR+cat:nlin.CD+OR+cat:nlin.CG+OR+cat:nlin.PS+OR+cat:nlin.SI+OR+cat:nucl-ex+OR+cat:nucl-th+OR+cat:physics.acc-ph+OR+cat:physics.ao-ph+OR+cat:physics.app-ph+OR+cat:physics.atm-clus+OR+cat:physics.atom-ph+OR+cat:physics.bio-ph+OR+cat:physics.chem-ph+OR+cat:physics.class-ph+OR+cat:physics.comp-ph+OR+cat:physics.data-an+OR+cat:physics.ed-ph+OR+cat:physics.flu-dyn+OR+cat:physics.gen-ph+OR+cat:physics.geo-ph+OR+cat:physics.hist-ph+OR+cat:physics.ins-det+OR+cat:physics.med-ph+OR+cat:physics.optics+OR+cat:physics.plasm-ph+OR+cat:physics.pop-ph+OR+cat:physics.soc-ph+OR+cat:physics.space-ph+OR+cat:q-bio.BM+OR+cat:q-bio.CB+OR+cat:q-bio.GN+OR+cat:q-bio.MN+OR+cat:q-bio.NC+OR+cat:q-bio.OT+OR+cat:q-bio.PE+OR+cat:q-bio.QM+OR+cat:q-bio.SC+OR+cat:q-bio.TO+OR+cat:q-fin.CP+OR+cat:q-fin.EC+OR+cat:q-fin.GN+OR+cat:q-fin.MF+OR+cat:q-fin.PM+OR+cat:q-fin.PR+OR+cat:q-fin.RM+OR+cat:q-fin.ST+OR+cat:q-fin.TR+OR+cat:quant-ph+OR+cat:stat.AP+OR+cat:stat.CO+OR+cat:stat.ME+OR+cat:stat.ML+OR+cat:stat.OT+OR+cat:stat.TH" --start-index $START_INDEX > log
	
	DONE=`cat log | grep "No new papers were added. Assuming no new papers exist. Exiting."`

	[[ -z $DONE ]] || break

	sleep 120
done
