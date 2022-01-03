# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import pickle
from collections import defaultdict

from normalise.detect import mod_path

abbrev_dict = {
               "abbrev.": "abbreviation",
               "abr.": "abridged",
               "abridg.": "abridged",
               "absol.": "absolute",
               "abst.": "abstract",
               "abstr.": "abstract",
               "accomm.": "accommodation",
               "accompl.": "accomplished",
               "acct.": "account",
               "accts.": "accounts",
               "addr.": "address",
               "adj.": "adjective",
               "adjs.": "adjectives",
               "adm.": "admiral",
               "adv.": "adverb",
               "advb.": "adverb",
               "advt.": "advertisement",
               "advts.": "advertisements",
               "aff.": "affairs",
               "afr.": "Africa",
               "agst.": "against",
               "alg.": "algebra",
               "alt.": "alteration",
               "ann.": "annual",
               "anniv.": "anniversary",
               "anon.": "anonymous",
               "answ.": "answer",
               "apol.": "apology",
               "apr.": "April",
               "arch.": "architecture",
               "argt.": "argument",
               "arith.": "arithmetic",
               "artific.": "artificial",
               "assemb.": "assembly",
               "assoc.": "association",
               "astr.": "astronomy",
               "attrib.": "attribute",
               "aug.": "August",
               "bef.": "before",
               "belg.": "Belgian",
               "betw.": "between",
               "biog.": "biography",
               "bk.": "book",
               "bks.": "books",
               "braz.": "Brazilian",
               "c.": "century",
               "c": "circa",
               "cal.": "calendar",
               "calc.": "calculus",
               "calif.": "California",
               "camb.": "Cambridge",
               "capt.": "captain",
               "cath.": "Catholic",
               "cent.": "century",
               "cert.": "certificate",
               "certif.": "certificate",
               "char.": "character",
               "circ.": "circle",
               "cl.": "clause",
               "co.": "company",
               "col.": "colonel",
               "coll.": "college",
               "colloq.": "colloquial",
               "comb.": "combination",
               "combs.": "combinations",
               "commerc.": "commercial",
               "commonw.": "commonwealth",
               "conc.": "concerning",
               "concl.": "conclusion",
               "conf.": "conference",
               "congr.": "congress",
               "conj.": "conjunction",
               "conn.": "Connecticut",
               "cons.": "consonant",
               "constr.": "construction",
               "contemp.": "contemporary",
               "cont.": "continuation",
               "contrib.": "contribution",
               "conv.": "convention",
               "counc.": "council",
               "cmpd.": "compound",
               "crim.": "criminal",
               "crt.": "court",
               "crts.": "courts",
               "dec.": "December",
               "dept.": "department",
               "devel.": "development",
               "dict.": "dictionary",
               "dist.": "district",
               "distrib.": "distribution",
               "dk.": "Duke",
               "docs.": "documents",
               "doc.": "document",
               "dr.": "Doctor",
               "e.": "east",
               "eds.": "editions",
               "ed.": "edition",
               "edw.": "Edward",
               "emb.": "embassy",
               "encycl.": "encyclopaedia",
               "enq.": "enquiry",
               "equip.": "equipment",
               "esp.": "especially",
               "eval.": "evaluation",
               "evid.": "evidence",
               "exam.": "examination",
               "exc.": "except",
               "exch.": "exchange",
               "exerc.": "exercise",
               "f.": "feminine",
               "feb.": "February",
               "fem.": "feminine",
               "figs.": "figures",
               "fig.": "figure",
               "freq.": "frequently",
               "gd.": "good",
               "gen.": "general",
               "geog.": "geography",
               "gloss.": "glossary",
               "govt.": "government",
               "gr.": "grammar",
               "gt.": "great",
               "handbk.": "handbook",
               "hist.": "historical",
               "hosp.": "hospital",
               "husb.": "husband",
               "inc.": "incorporated",
               "ind.": "industry",
               "indef.": "indefinite",
               "inq.": "inquiry",
               "intro.": "introduction",
               "inv.": "inventory",
               "investig.": "investigation",
               "investm.": "investment",
               "irel.": "Ireland",
               "irreg.": "irregular",
               "jan.": "January",
               "jr.": "junior",
               "jrnl.": "journal",
               "jrnls.": "journals",
               "jul.": "July",
               "jun.": "June",
               "k.": "king",
               "kingd.": "kingdom",
               "knowl.": "knowledge",
               "lab.": "laboratory",
               "lang.": "language",
               "langs.": "languages",
               "lat.": "Latin",
               "ld.": "Lord",
               "lds.": "Lords",
               "lect.": "lecture",
               "let.": "letter",
               "letts.": "letters",
               "libr.": "library",
               "ling.": "linguistic",
               "lt.": "Lieutenant",
               "m.": "masculine",
               "mag.": "magazine",
               "man.": "manual",
               "mar.": "March",
               "masc.": "masculine",
               "meas.": "measure",
               "med.": "medieval",
               "mem.": "memoir",
               "merch.": "merchandise",
               "meth.": "method",
               "mil.": "military",
               "milit.": "military",
               "mispr.": "misprinted",
               "mod.": "modern",
               "MS.": "manuscript",
               "mtg.": "meeting",
               "mts.": "mountains",
               "mus.": "museum",
               "myst.": "mystery",
               "myth.": "mythology",
               "narr.": "narrative",
               "nat.": "natural",
               "naut.": "nautical",
               "nav.": "naval",
               "navig.": "navigation",
               "neurol.": "neurology",
               "no.": "number",
               "norweg.": "Norwegian",
               "nov.": "November",
               "num.": "Numbers",
               "N.Z.": "New Zealand",
               "observ.": "observation",
               "occas.": "occasion",
               "occurr.": "occurrence",
               "oct.": "October",
               "O.E.D.": "Oxford English Dictionary",
               "offic.": "official",
               "org.": "organic",
               "orig.": "original",
               "oxf.": "Oxford",
               "p.": "page",
               "pass.": "passive",
               "perf.": "perfect",
               "pers.": "personal",
               "photog.": "photography",
               "photogr.": "photography",
               "phr.": "phrase",
               "pict.": "picture",
               "pl.": "plural",
               "plur.": "plural",
               "pop.": "popular",
               "ppl.": "people",
               "pr.": "present",
               "prec.": "preceding",
               "pred.": "prediction",
               "pref.": "prefix",
               "prob.": "probably",
               "probl.": "problem",
               "prod.": "product",
               "pron.": "pronoun",
               "pronunc.": "pronunciation",
               "prop.": "properly",
               "prov.": "proverb",
               "provid.": "providence",
               "provinc.": "provincial",
               "psych.": "psychology",
               "pt.": "part",
               "q.": "quarterly",
               "Q.": "queen",
               "quot.": "quotation",
               "quots.": "quotations",
               "R.C.": "Roman Catholic",
               "rd.": "road",
               "ref.": "reference",
               "regist.": "register",
               "rel.": "relative",
               "rept.": "report",
               "repub.": "republic",
               "ret.": "return",
               "revol.": "revolution",
               "rich.": "Richard",
               "R.N.": "Royal Navy",
               "rom.": "Roman",
               "s.": "south",
               "sat.": "Saturday",
               "sax.": "Saxon",
               "sch.": "school",
               "scot.": "Scottish",
               "scotl.": "Scotland",
               "sen.": "Senator",
               "sept.": "September",
               "sess.": "session",
               "settlem.": "settlement",
               "sev.": "several",
               "soc.": "society",
               "sp.": "spelling",
               "span.": "Spanish",
               "spec.": "specimen",
               "std.": "standard",
               "stand.": "standard",
               "str.": "strong",
               "subj.": "subject",
               "subord.": "subordinate",
               "syll.": "syllable",
               "symmetr.": "symmetrical",
               "syst.": "system",
               "techn.": "technical",
               "telecomm.": "telecommunications",
               "test.": "testament",
               "textbk.": "textbook",
               "thes.": "thesaurus",
               "trag.": "tragedy",
               "transf.": "transfer",
               "transl.": "translation",
               "treatm.": "treatment",
               "trig.": "trigonometry",
               "trop.": "tropical",
               "typogr.": "typography",
               "U.K.": "United Kingdom",
               "univ.": "university",
               "unkn.": "unknown",
               "unoffic.": "unofficial",
               "vac.": "vacation",
               "var.": "variant",
               "vb.": "verb",
               "vbl.": "verbal",
               "vbs.": "verbs",
               "veg.": "vegetable",
               "vic.": "Victoria",
               "vict.": "Victoria",
               "vocab.": "vocabulary",
               "vol.": "volume",
               "vols.": "volumes",
               "w.": "west",
               "wd.": "word",
               "wis.": "Wisconsin",
               "wkly.": "weekly",
               "wks.": "works",
               "yearbk.": "yearbook",
               "yng.": "young",
               "yr.": "year",
               "yrs.": "years"
               }


ambig_abbrevs = {
                 "acad.": ["academia", "academy", "academic"],
                 "acc.": ["according", "account"],
                 "admin.": ["administration", "administrative"],
                 "adv.": ["advanced", "adventure"],
                 "agric.": ["agriculture", "agricultural"],
                 "amer.": ["America", "American"],
                 "art.": ["article", "artifact"],
                 "biochem.": ["biochemistry", "biochemical"],
                 "chem.": ["chemistry", "chemical"],
                 "chron.": ["chronology", "chronicle"],
                 "comm.": ["commerce", "committee"],
                 "corresp.": ["corresponding", "correspondence"],
                 "crit.": ["critical", "criticism"],
                 "ct.": ["count", "court"],
                 "def.": ["definite", "definition"],
                 "dep.": ["department", "deputy"],
                 "descr.": ["description", "descriptive"],
                 "e.": ["east", "eastern"],
                 "ecol.": ["ecology", "ecological"],
                 "econ.": ["economics", "economical"],
                 "educ.": ["education", "educational"],
                 "electr.": ["electricity", "electrical"],
                 "fam.": ["familiar", "family"],
                 "eng.": ["England", "English"],
                 "fr.": ["French", "France"],
                 "geogr.": ["geography", "geographical"],
                 "geol.": ["geology", "geological"],
                 "geom.": ["geometry", "geometrical"],
                 "ger.": ["German", "Germany"],
                 "gov.": ["government", "Governor"],
                 "hist.": ["history", "historical"],
                 "illustr.": ["illustrated", "illustration"],
                 "ind.": ["India", "Indian"],
                 "industr.": ["industrial", "industry"],
                 "inst.": ["institute", "institution"],
                 "intell.": ["intelligence", "intelligent"],
                 "introd.": ["introduction", "introductory"],
                 "ital.": ["Italian", "Italy"],
                 "jap.": ["Japanese", "Japan"],
                 "lit.": ["literal", "literally"],
                 "lit.": ["literary", "literature"],
                 "mach.": ["machinery", "machine"],
                 "math.": ["mathematics", "mathematical"],
                 "mech.": ["mechanics", "mechanical"],
                 "med.": ["medicine", "medical"],
                 "mex.": ["Mexican", "Mexico"],
                 "misc.": ["miscellaneous", "miscellany"],
                 "mt.": ["mount", "mountain"],
                 "mus.": ["music", "musical"],
                 "n.": ["north", "northern"],
                 "n.e.": ["north-east", "north-eastern"],
                 "n.w.": ["north-west", "north-western"],
                 "obj.": ["object", "objective"],
                 "occup.": ["occupation", "occupational"],
                 "off.": ["official", "office"],
                 "opp.": ["opposed", "opposite"],
                 "orig.": ["origin", "original"],
                 "parl.": ["parliament", "parliamentary"],
                 "perf.": ["perfect", "perfection"],
                 "phil.": ["philosophy", "philosophical"],
                 "phys.": ["physiology", "physics"],
                 "physiol.": ["physiology", "physiological"],
                 "pol.": ["politics", "political"],
                 "polit.": ["politics", "political"],
                 "port.": ["Portuguese", "Portugal"],
                 "poss.": ["possible", "possibly"],
                 "pract.": ["practical", "practice"],
                 "pres.": ["President", "present"],
                 "princ.": ["principle", "principality"],
                 "probab.": ["probability", "probably"],
                 "prop.": ["property", "proper"],
                 "psychol.": ["psychology", "psychological"],
                 "publ.": ["public", "publication"],
                 "rec.": ["record", "recording"],
                 "reg.": ["regular", "register"],
                 "rep.": ["report", "representative"],
                 "repr.": ["representative", "representing"],
                 "resid.": ["residence", "residential"],
                 "rev.": ["Reverend", "revised", "review"],
                 "russ.": ["Russia", "Russian"],
                 "s.": ["south", "southern"],
                 "scand.": ["Scandinavia", "Scandinavian"],
                 "sci.": ["science", "scientific"],
                 "s.e.": ["south-east", "south-eastern"],
                 "sociol.": ["sociology", "sociological"],
                 "st.": ["Saint", "street"],
                 "struct.": ["structure", "structural"],
                 "suppl.": ["supplement", "supplementary"],
                 "surg.": ["surgery", "surgical"],
                 "surv.": ["survey", "surveying"],
                 "s.w.": ["south-west", "south-western"],
                 "technol.": ["technology", "technological"],
                 "tel.": ["telegraph", "telephone"],
                 "teleph.": ["telephone", "telephony", "telephonic"],
                 "theol.": ["theology", "theological"],
                 "tr.": ["translation", "translating"],
                 "trad.": ["tradition", "traditional"],
                 "transl.": ["translation", "translating"],
                 "treas.": ["treasurer", "treasury"],
                 "w.": ["west", "western"],
                 "wk.": ["week", "work"]
                 }


states = {
          "Ala.": "Alabama",
          "Alaska": "Alaska",
          "Ariz.": "Arizona",
          "Ark.": "Arkansas",
          "Calif.": "California",
          "Colo.": "Colorado",
          "Conn.": "Connecticut",
          "Del.": "Delaware",
          "D.C.": "Dist. of Columbia",
          "Fla.": "Florida",
          "Ga.": "Georgia",
          "Ill.": "Illinois",
          "Ind.": "Indiana",
          "Kans.": "Kansas",
          "Ky.": "Kentucky",
          "La.": "Louisiana",
          "Md.": "Maryland",
          "Mass.": "Massachusetts",
          "Mich.": "Michigan",
          "Minn.": "Minnesota",
          "Miss.": "Mississippi",
          "Mo.": "Missouri",
          "Mont.": "Montana",
          "Nebr.": "Nebraska",
          "Nev.": "Nevada",
          "N.H.": "New Hampshire",
          "N.J.": "New Jersey",
          "N.M.": "New Mexico",
          "N.Y.": "New York",
          "N.C.": "North Carolina",
          "N.D.": "North Dakota",
          "Okla.": "Oklahoma",
          "Ore.": "Oregon",
          "Pa.": "Pennsylvania",
          "P.R.": "Puerto Rico",
          "R.I.": "Rhode Island",
          "S.C.": "South Carolina",
          "S.D.": "South Dakota",
          "Tenn.": "Tennessee",
          "Tex.": "Texas",
          "Vt.": "Vermont",
          "Va.": "Virginia",
          "V.I.": "Virgin Islands",
          "Wash.": "Washington",
          "W.Va.": "West Virginia",
          "Wis.": "Wisconsin",
          "Wyo.": "Wyoming"
          }

titles = {
          "lt.": "Lieutenant",
          "rt.": "right",
          "hon.": "Honourable",
          "supt.": "Superintendent",
          "sr.": "senior"
          }


def build_abbrevs(dictionary):
    """Builds abbreviation dictionary from input in correct format."""
    abbrevs = defaultdict(list)
    for key in dictionary:
        if key.endswith('.'):
            k = key[:-1].lower()
        else:
            k = key.lower()
        if type(dictionary[key]) == list:
            abbrevs[k].extend(dictionary[key])
        elif type(dictionary[key]) == str:
            abbrevs[k].append(dictionary[key])
    return abbrevs


def create_user_abbrevs(dictionary):
    """Stores user and general abbreviations in pickle file."""
    with open('{}/data/abbrev_dict.pickle'.format(mod_path), mode='rb') as f:
        abbrevs = pickle.load(f)
    for key in dictionary:
        if key.endswith('.'):
            k = key[:-1].lower()
        else:
            k = key.lower()
        if type(dictionary[key]) == list:
            for exp in dictionary[key]:
                if exp not in abbrevs[k]:
                    abbrevs[k].append(exp)
        elif type(dictionary[key]) == str:
            if dictionary[key] not in abbrevs[k]:
                abbrevs[k].append(dictionary[key])
    return abbrevs


def add_to_pickled_abbrev(dictionary):
    """Add new dictionary to pickled file of abbreviations."""
    with open('{}/data/abbrev_dict.pickle'.format(mod_path), mode='rb') as f:
        abbrevs = pickle.load(f)
    for key in dictionary:
        if key.endswith('.'):
            k = key[:-1].lower()
        else:
            k = key.lower()
        if type(dictionary[key]) == list:
            for exp in dictionary[key]:
                if exp not in abbrevs[k]:
                    abbrevs[k].append(exp)
        elif type(dictionary[key]) == str:
            if dictionary[key] not in abbrevs[k]:
                abbrevs[k].append(dictionary[key])
    with open('{}/data/abbrev_dict.pickle'.format(mod_path), mode='wb') as f:
        pickle.dump(abbrevs, f, protocol=2)
    print(abbrevs)
