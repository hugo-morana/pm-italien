/* ============ Palais « Lisa » : la maison familiale ============
   Même contenu et même ordre que le palais par classe (liens de chaîne intacts), mais chaque salle de 100 niches
   devient une pièce familière d'une maison, chaque fois différente : entrée, salon, cuisine, chambres, salle de bain,
   toilettes, grenier, cave, garage, jardin, piscine, terrasse… Les 10 surfaces deviennent 10 objets typiques de la
   pièce (« il divano · le canapé »), modélisés à côté de leur panneau : on accroche chaque dizaine à un objet. */
const HOMES = [
  { k: "ingresso", fr: "Entrée", it: "L'ingresso", wall: "#d9c7a6", floor: ["damier", "#2b2b2b", "#e8e2d4"], ceil: "#f2ece0", land: "plante", o: [
    ["l'appendiabiti · le portemanteau", "portemanteau", "T"], ["la console · la console", "console"], ["la porta d'ingresso · la porte d'entrée", "porte", "T"], ["la scarpiera · le meuble à chaussures", "scarpiera"], ["l'orologio a pendolo · l'horloge", "horloge", "T"],
    ["lo zerbino · le paillasson", "paillasson"], ["il pacco · le colis", "cartons"], ["il portaombrelli · le porte-parapluie", "parapluies"], ["la plafoniera · le plafonnier", "plafonnier"], ["il rilevatore di fumo · le détecteur de fumée", "detecteur"]] },
  { k: "soggiorno", fr: "Salon", it: "Il soggiorno", wall: "#c97b5a", floor: ["parquet", "#9a6b40", "#b5824f"], ceil: "#f3e9d8", land: "fauteuil", o: [
    ["il divano · le canapé", "canape"], ["il camino · la cheminée", "cheminee"], ["la televisione · la télévision", "tv"], ["la pianta · la plante verte", "plante"], ["la libreria · la bibliothèque", "biblio", "T"],
    ["il pouf · le pouf", "pouf"], ["il tavolino · la table basse", "tablebasse"], ["il tappeto · le tapis", "tapis"], ["il lampadario · le lustre", "lustre"], ["il ventilatore · le ventilateur", "ventilo"]] },
  { k: "pranzo", fr: "Salle à manger", it: "La sala da pranzo", wall: "#7a8f6a", floor: ["parquet", "#6e4a2c", "#7f5634"], ceil: "#efe9dc", land: "horloge", o: [
    ["la credenza · le buffet", "buffet"], ["la vetrina · le vaisselier", "vaisselier"], ["la finestra · la fenêtre", "fenetre", "T"], ["il vaso di fiori · le vase de fleurs", "vase"], ["il carrello · la desserte", "desserte"],
    ["le sedie · les chaises", "chaises"], ["la tavola apparecchiata · la table mise", "table"], ["la panca · le banc", "banc"], ["la lampada a sospensione · la suspension", "suspension"], ["la ghirlanda · la guirlande", "guirlande"]] },
  { k: "cucina", fr: "Cuisine", it: "La cucina", wall: "#f0dc78", floor: ["damier", "#b8463a", "#efe6d6"], ceil: "#fbf7ec", land: "fruits", o: [
    ["il frigorifero · le réfrigérateur", "frigo", "T"], ["il microonde · le micro-ondes", "microonde"], ["il lavello · l'évier", "evier"], ["la pattumiera · la poubelle", "poubelle"], ["i fornelli · la cuisinière", "cuisiniere"],
    ["la lavastoviglie · le lave-vaisselle", "lavevaisselle"], ["l'isola · l'îlot de cuisine", "ilot"], ["gli sgabelli · les tabourets", "tabourets"], ["la cappa · la hotte", "hotte"], ["le pentole appese · les casseroles suspendues", "casseroles"]] },
  { k: "lavanderia", fr: "Buanderie", it: "La lavanderia", wall: "#a9d3df", floor: ["carreaux", "#d6dde0", "#9fb0b8"], ceil: "#eef4f6", land: "aspirateur", o: [
    ["la lavatrice · le lave-linge", "lavelinge"], ["il detersivo · la lessive", "bidons"], ["l'asciugatrice · le sèche-linge", "sechelinge"], ["il cesto della biancheria · le panier à linge", "panier"], ["la caldaia · le chauffe-eau", "chaudiere", "T"],
    ["il ferro da stiro · le fer à repasser", "fer"], ["la bacinella · la bassine", "bassine"], ["la scopa · le balai", "balai"], ["lo stendino · l'étendoir", "etendoir"], ["le mollette · les pinces à linge", "pinces"]] },
  { k: "studio", fr: "Bureau", it: "Lo studio", wall: "#3f6273", floor: ["parquet", "#4a3524", "#5a412c"], ceil: "#e8e4dc", land: "lampadaire", o: [
    ["la scrivania · le bureau", "bureau"], ["la stampante · l'imprimante", "imprimante"], ["lo scaffale · l'étagère", "biblio", "T"], ["il mappamondo · le globe", "globe"], ["la cassettiera · le caisson", "caisson"],
    ["la sedia girevole · le fauteuil de bureau", "fauteuilbureau"], ["il tappeto · le tapis", "tapis"], ["il cestino · la corbeille", "poubelle"], ["i faretti · les spots", "spots"], ["il condizionatore · le climatiseur", "clim"]] },
  { k: "camera", fr: "Chambre des parents", it: "La camera da letto", wall: "#b9a3c9", floor: ["moquette", "#cdb9a6", "#bca792"], ceil: "#f5f0f7", land: "valise", o: [
    ["l'armadio · l'armoire", "armoire", "T"], ["il comodino · la table de chevet", "chevet"], ["la testiera · la tête de lit", "tetelit"], ["la toeletta · la coiffeuse", "coiffeuse"], ["il cassettone · la commode", "commode"],
    ["le pantofole · les chaussons", "chaussons"], ["il letto matrimoniale · le lit double", "lit"], ["lo scendiletto · la descente de lit", "tapis"], ["il lampadario · le lustre", "lustre"], ["la zanzariera · la moustiquaire", "moustiquaire"]] },
  { k: "cameretta", fr: "Chambre d'enfant", it: "La cameretta", wall: "#8fd0a8", floor: ["damier", "#f2c84b", "#5aa0d8"], ceil: "#cfe6ff", land: "trottinette", o: [
    ["la cassapanca dei giochi · le coffre à jouets", "coffre"], ["l'orsacchiotto · l'ours en peluche", "ours"], ["la casa delle bambole · la maison de poupée", "maisonpoupee"], ["il cavallo a dondolo · le cheval à bascule", "cheval"], ["il letto a castello · les lits superposés", "litsup", "T"],
    ["il pallone · le ballon", "ballon"], ["il tappeto puzzle · le tapis puzzle", "tapispuzzle"], ["il trenino · le petit train", "train"], ["la giostrina · le mobile", "mobile"], ["le stelle · les étoiles", "etoiles"]] },
  { k: "bagno", fr: "Salle de bain", it: "Il bagno", wall: "#8fcbe0", floor: ["damier", "#ffffff", "#2f6f9a"], ceil: "#f7fbfc", land: "plante", o: [
    ["la vasca da bagno · la baignoire", "baignoire"], ["il portasciugamani · le porte-serviettes", "radiateur"], ["il lavandino · le lavabo", "lavabo"], ["lo spazzolino · la brosse à dents", "verre"], ["la doccia · la douche", "douche", "T"],
    ["la bilancia · la balance", "balance"], ["il tappetino · le tapis de bain", "tapisbain"], ["il cesto · le panier à linge", "panier"], ["il neon · le néon", "neon"], ["la tenda della doccia · le rideau de douche", "rideaudouche"]] },
  { k: "gabinetto", fr: "Toilettes", it: "Il gabinetto", wall: "#2e6b4f", floor: ["damier", "#1e1e1e", "#d0d0d0"], ceil: "#f0f0ea", land: "plante", o: [
    ["il water · la cuvette", "wc"], ["la carta igienica · le papier toilette", "papier"], ["lo sciacquone · la chasse d'eau", "chasse"], ["lo scopino · la balayette", "balayette"], ["il lavamani · le lave-mains", "lavabo"],
    ["le riviste · les magazines", "magazines"], ["il deodorante · le désodorisant", "spray"], ["il tappetino · le tapis", "tapisbain"], ["la lampadina · l'ampoule", "ampoule"], ["la finestrella · la lucarne", "lucarne"]] },
  { k: "soffitta", fr: "Grenier", it: "La soffitta", wall: "#9b7a55", floor: ["planches", "#7b5a3a", "#6a4c30"], ceil: "#5a4030", land: "velo", o: [
    ["il baule · la malle", "malle"], ["le scatole · les cartons", "cartons"], ["l'abbaino · la lucarne", "fenetre", "T"], ["la sedia a dondolo · le rocking-chair", "fauteuil"], ["il manichino · le mannequin", "mannequin", "T"],
    ["il grammofono · le gramophone", "gramo"], ["il tappeto arrotolato · le tapis roulé", "rouleau"], ["la bambola · la poupée", "poupee"], ["la trave · la poutre", "poutre"], ["la ragnatela · la toile d'araignée", "toile"]] },
  { k: "cantina", fr: "Cave", it: "La cantina", wall: "#6b6460", floor: ["pierre", "#5e5751", "#4a4440"], ceil: "#3d3732", land: "tonneau", o: [
    ["la rastrelliera · le casier à bouteilles", "vins", "T"], ["la botte · le tonneau", "tonneau"], ["la caldaia · la chaudière", "chaudiere", "T"], ["il secchio · le seau", "seau"], ["gli scaffali · les étagères", "etagere", "T"],
    ["le casse d'acqua · les packs d'eau", "cartons"], ["la cassetta di mele · la cagette de pommes", "cagette"], ["la trappola per topi · la tapette à souris", "tapette"], ["il prosciutto appeso · le jambon suspendu", "jambon"], ["la lampadina · l'ampoule nue", "ampoule"]] },
  { k: "garage", fr: "Garage", it: "Il garage", wall: "#9a9a9a", floor: ["beton", "#8f8f8c", "#7a7a77"], ceil: "#cfcfcf", land: "velo", o: [
    ["il pannello degli attrezzi · le panneau à outils", "outils"], ["la tanica · le bidon d'essence", "bidon"], ["la saracinesca · la porte de garage", "portegarage", "T"], ["la scala · l'escabeau", "escabeau"], ["la macchina · la voiture", "voiture", "T"],
    ["la cassetta degli attrezzi · la caisse à outils", "caisse"], ["il banco da lavoro · l'établi", "etabli"], ["le gomme · les pneus", "pneus"], ["il neon · le néon", "neon"], ["la bici appesa · le vélo suspendu", "velosusp"]] },
  { k: "giardino", fr: "Jardin", it: "Il giardino", out: true, wall: "#4f7f3a", floor: ["gazon", "#5f9a3f", "#4d8434"], ceil: "#9cc8ec", land: "arrosoir", o: [
    ["la siepe · la haie", "haie"], ["la cuccia · la niche du chien", "niche"], ["l'albero · l'arbre", "arbre", "T"], ["il nano da giardino · le nain de jardin", "nain"], ["il barbecue · le barbecue", "bbq"],
    ["l'aiuola · le parterre de fleurs", "fleurs"], ["il tavolo da giardino · la table de jardin", "tablejardin"], ["la carriola · la brouette", "brouette"], ["il sole · le soleil", "soleil"], ["la nuvola · le nuage", "nuage"]] },
  { k: "piscina", fr: "Piscine", it: "La piscina", out: true, wall: "#dfe9ee", floor: ["carreaux", "#e6eef0", "#bcd3da"], ceil: "#a8d8f4", land: "plante", o: [
    ["la doccia esterna · la douche extérieure", "douche", "T"], ["l'asciugamano · la serviette", "serviette"], ["il trampolino · le plongeoir", "plongeoir"], ["il salvagente · la bouée", "bouee"], ["la sdraio · le transat", "transat"],
    ["il materassino · le matelas gonflable", "matelas"], ["la vasca · le bassin", "bassin"], ["la scaletta · l'échelle de piscine", "echelle"], ["l'ombrellone · le parasol", "parasol"], ["il gabbiano · la mouette", "oiseau"]] },
  { k: "terrazza", fr: "Terrasse", it: "La terrazza", out: true, wall: "#e7c9a0", floor: ["planches", "#a07850", "#8a6440"], ceil: "#f4c58a", land: "plante", o: [
    ["il limone in vaso · le citronnier en pot", "citronnier"], ["l'amaca · le hamac", "hamac"], ["la ringhiera · la rambarde", "rambarde"], ["la lanterna · la lanterne", "lanterne"], ["il dondolo · la balancelle", "balancelle"],
    ["i cuscini · les coussins", "coussins"], ["il tavolino · la petite table", "tablebasse"], ["l'annaffiatoio · l'arrosoir", "arrosoir"], ["la tenda da sole · le store banne", "store"], ["la luna · la lune", "lune"]] }
];
// une teinte et un style par appartement (étage), pour que deux salons ne se confondent pas
const HSTYLES = [["classique", "#ffffff", 0], ["provençal", "#f2b56b", .22], ["scandinave", "#ffffff", .35], ["bord de mer", "#6fb3d9", .22], ["montagne", "#8a5a33", .22], ["années 70", "#e0892b", .28], ["art déco", "#1f3b4d", .2]];
function mixHex(a, b, t) { const p = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16)); const A = p(a), B = p(b); return "#" + A.map((v, i) => Math.round(v + (B[i] - v) * t).toString(16).padStart(2, "0")).join(""); }
function applyLisa() {   // pièces de la maison, 16 par étage (8 de chaque côté du couloir), dans l'ordre du palais par classe
  R.forEach((r, ri) => {
    const fl = Math.floor(ri / 16), j = ri % 16, H = HOMES[j], st = HSTYLES[fl % HSTYLES.length];
    r.home = Object.assign({}, H, { wall: mixHex(H.wall, st[1], st[2]), style: st[0], apt: fl + 1 });
    r.cls = { fr: r.fr, it: r.it }; r.fr = `${H.fr} — ${r.fr}`; r.it = H.it; r.blocs = H.o.map(o => o[0]);
    r.slot = { floor: fl, side: j < 8 ? "N" : "S", x: j % 8 };
  });
}
/* --- mobilier : primitives [type, a, b, c, couleur, x, y, z, rx, ry, rz] ; b = boîte l×h×p, c = cylindre r1 r2 h, s = sphère r, k = cône r h, t = tore R r
   origine au sol, face avant vers +z ; plafond : origine au plafond, y négatif */
const FURN = {
  portemanteau: [["c", .05, .05, 1.9, "#5b3a26", 0, .95, 0], ["c", .3, .35, .05, "#5b3a26", 0, .03, 0], ["c", .02, .02, .5, "#5b3a26", .2, 1.75, 0, 0, 0, 1], ["c", .02, .02, .5, "#5b3a26", -.2, 1.75, 0, 0, 0, -1], ["b", .5, .7, .15, "#2f5fae", .25, 1.35, .1], ["b", .45, .5, .2, "#c8302c", -.22, 1.45, .05]],
  console: [["b", 1.4, .06, .4, "#7a4a2a", 0, .85, 0], ["b", .05, .85, .05, "#5b3a26", -.65, .42, .15], ["b", .05, .85, .05, "#5b3a26", .65, .42, .15], ["b", .05, .85, .05, "#5b3a26", -.65, .42, -.15], ["b", .05, .85, .05, "#5b3a26", .65, .42, -.15], ["c", .12, .08, .1, "#c9a24a", .4, .93, 0], ["b", .3, .03, .2, "#c9a24a", -.3, .9, 0]],
  porte: [["b", 1.2, 2.3, .08, "#7a4a2a", 0, 1.15, 0], ["b", 1.36, .1, .12, "#4a3020", 0, 2.35, 0], ["s", .05, 0, 0, "#c9a24a", .45, 1.1, .08], ["b", .7, .5, .02, "#a8723f", 0, 1.7, .05], ["b", .7, .5, .02, "#a8723f", 0, .6, .05]],
  scarpiera: [["b", 1.3, .55, .4, "#e8dcc6", 0, .28, 0], ["b", .25, .1, .1, "#2a211d", -.4, .6, .05], ["b", .25, .1, .1, "#c8302c", -.1, .6, .05], ["b", .25, .1, .1, "#2f5fae", .25, .6, .05]],
  horloge: [["b", .6, 2.1, .4, "#5b3a26", 0, 1.05, 0], ["c", .22, .22, .05, "#f4f1ea", 0, 1.7, .21, 1.57], ["c", .02, .02, .7, "#c9a24a", 0, .9, .21], ["c", .1, .1, .04, "#c9a24a", 0, .55, .21, 1.57]],
  paillasson: [["b", 2.2, .06, 1.6, "#8a6a3a", 0, .03, 0], ["b", 1.6, .065, .3, "#5b3a26", 0, .035, 0]],
  cartons: [["b", .9, .6, .7, "#c49a63", -.5, .3, 0], ["b", .7, .5, .6, "#b88b52", .4, .25, .1], ["b", .6, .4, .5, "#d1a873", -.4, .8, 0], ["b", .9, .03, .05, "#d9c8a4", -.5, .61, 0]],
  parapluies: [["c", .25, .22, .6, "#3f8f45", 0, .3, 0], ["c", .02, .02, .9, "#2a211d", -.07, .7, 0, .1], ["c", .02, .02, .9, "#c8302c", .07, .7, .05, -.1], ["k", .12, .3, "#c8302c", .07, .9, .05]],
  plafonnier: [["c", .02, .02, .4, "#555", 0, -.2, 0], ["s", .35, 0, 0, "#fff3c4", 0, -.55, 0]],
  detecteur: [["c", .25, .25, .08, "#f4f1ea", 0, -.04, 0], ["s", .04, 0, 0, "#c8302c", 0, -.1, 0]],
  plante: [["c", .3, .22, .55, "#b9603d", 0, .28, 0], ["s", .45, 0, 0, "#3f8f45", 0, .95, 0], ["s", .3, 0, 0, "#4d9f52", .2, 1.25, .1], ["s", .3, 0, 0, "#357a3a", -.2, 1.2, -.1]],
  canape: [["b", 2.3, .45, .9, "#5b6f8a", 0, .35, 0], ["b", 2.3, .55, .22, "#4d5f78", 0, .8, -.34], ["b", .22, .35, .9, "#4d5f78", -1.1, .7, 0], ["b", .22, .35, .9, "#4d5f78", 1.1, .7, 0], ["b", .5, .4, .15, "#e6c21f", -.6, .75, -.2], ["b", .5, .4, .15, "#c8302c", .6, .75, -.2]],
  cheminee: [["b", 1.8, 1.2, .5, "#d6c9b4", 0, .6, 0], ["b", 1.0, .75, .52, "#2a211d", 0, .4, .01], ["b", 2.0, .1, .6, "#bfae95", 0, 1.22, 0], ["k", .18, .4, "#e57a1e", -.15, .25, .1], ["k", .15, .3, "#e6c21f", .15, .2, .1]],
  tv: [["b", 1.8, .5, .45, "#2a211d", 0, .25, 0], ["b", 1.4, .7, .06, "#111", 0, .9, 0], ["b", 1.3, .6, .01, "#2f5fae", 0, .9, .04]],
  biblio: [["b", 1.6, 2.4, .4, "#7a4a2a", 0, 1.2, 0], ...[.4, .9, 1.4, 1.9].map(y => ["b", 1.5, .04, .38, "#5b3a26", 0, y, .01]), ...[0, 1, 2, 3].flatMap(k => [["b", .5, .35, .3, ["#c8302c", "#2f5fae", "#e6c21f", "#3f8f45"][k], -.4 + (k % 2) * .5, .6 + k * .5, .03], ["b", .35, .3, .3, ["#7d4aa3", "#e57a1e", "#f4f1ea", "#c8302c"][k], .4 - (k % 2) * .2, .58 + k * .5, .03]])],
  pouf: [["c", .45, .45, .45, "#c8302c", 0, .23, 0], ["c", .44, .44, .02, "#e6c21f", 0, .46, 0]],
  tablebasse: [["b", 1.6, .08, .9, "#a8723f", 0, .42, 0], ...[[-.7, -.35], [.7, -.35], [-.7, .35], [.7, .35]].map(([x, z]) => ["c", .04, .04, .4, "#5b3a26", x, .2, z]), ["c", .08, .08, .15, "#f4f1ea", .3, .53, 0]],
  tapis: [["b", 2.4, .02, 2.8, "#8e1c22", 0, .01, 0], ["b", 2.0, .025, 2.4, "#c9a24a", 0, .012, 0], ["b", 1.6, .03, 2.0, "#8e1c22", 0, .014, 0]],
  lustre: [["c", .02, .02, .5, "#c9a24a", 0, -.25, 0], ["t", .45, .04, 0, "#c9a24a", 0, -.55, 0, 1.57], ...[0, 1, 2, 3, 4, 5].map(k => ["s", .08, 0, 0, "#fff3c4", Math.cos(k) * .45, -.45, Math.sin(k) * .45])],
  ventilo: [["c", .03, .03, .3, "#555", 0, -.15, 0], ["c", .12, .12, .12, "#f4f1ea", 0, -.35, 0], ["b", 1.6, .02, .18, "#a8723f", 0, -.4, 0], ["b", .18, .02, 1.6, "#a8723f", 0, -.4, 0]],
  fauteuil: [["b", 1.1, .45, .9, "#6b2d3a", 0, .35, 0], ["b", 1.1, .9, .2, "#6b2d3a", 0, .9, -.35], ["b", .2, .3, .9, "#55222e", -.55, .7, 0], ["b", .2, .3, .9, "#55222e", .55, .7, 0]],
  buffet: [["b", 2.0, .9, .5, "#6e4a2c", 0, .45, 0], ["b", .9, .7, .02, "#8a5a33", -.48, .45, .26], ["b", .9, .7, .02, "#8a5a33", .48, .45, .26], ["c", .15, .1, .3, "#2f5fae", .5, 1.05, 0]],
  vaisselier: [["b", 1.4, 1.2, .45, "#e8dcc6", 0, .6, 0], ...[.3, .7, 1.0].flatMap(y => [-.4, 0, .4].map(x => ["c", .14, .14, .02, "#2f5fae", x, y + .15, .18, 1.57]))],
  fenetre: [["b", 1.6, 1.8, .08, "#f4f1ea", 0, 1.6, 0], ["b", 1.4, 1.6, .02, "#9cc8ec", 0, 1.6, .04], ["b", .06, 1.6, .05, "#f4f1ea", 0, 1.6, .06], ["b", 1.4, .06, .05, "#f4f1ea", 0, 1.6, .06], ["b", .4, 2.0, .06, "#c8302c", -1.0, 1.55, .1], ["b", .4, 2.0, .06, "#c8302c", 1.0, 1.55, .1]],
  vase: [["b", .8, .8, .5, "#7a4a2a", 0, .4, 0], ["c", .12, .18, .4, "#2f5fae", 0, 1.0, 0], ...[[-.15, "#c8302c"], [0, "#e6c21f"], [.15, "#e58fb2"]].map(([x, c]) => ["s", .1, 0, 0, c, x, 1.35, 0])],
  desserte: [["b", 1.0, .04, .5, "#c9a24a", 0, .8, 0], ["b", 1.0, .04, .5, "#c9a24a", 0, .35, 0], ...[[-.45, -.2], [.45, -.2], [-.45, .2], [.45, .2]].map(([x, z]) => ["c", .02, .02, .8, "#c9a24a", x, .45, z]), ["c", .06, .06, .3, "#3f8f45", -.2, .97, 0], ["c", .06, .06, .25, "#7a1f24", .15, .95, 0]],
  chaises: [...[-.8, .8].flatMap(x => [["b", .55, .06, .55, "#7a4a2a", x, .45, 0], ["b", .55, .6, .06, "#7a4a2a", x, .75, -.25], ["c", .03, .03, .45, "#5b3a26", x - .22, .22, .22], ["c", .03, .03, .45, "#5b3a26", x + .22, .22, .22]])],
  table: [["b", 2.2, .08, 1.4, "#8a5a33", 0, .66, 0], ["b", 2.3, .01, 1.5, "#f4f1ea", 0, .71, 0], ...[[-1, -.6], [1, -.6], [-1, .6], [1, .6]].map(([x, z]) => ["c", .05, .05, .62, "#5b3a26", x, .31, z]), ["c", .18, .18, .02, "#f4f1ea", -.5, .72, .3], ["c", .18, .18, .02, "#f4f1ea", .5, .72, .3]],
  banc: [["b", 2.0, .08, .45, "#7a4a2a", 0, .45, 0], ["b", .08, .45, .4, "#5b3a26", -.9, .22, 0], ["b", .08, .45, .4, "#5b3a26", .9, .22, 0]],
  suspension: [["c", .015, .015, .9, "#333", 0, -.45, 0], ["k", .35, .3, "#c8302c", 0, -1.05, 0], ["s", .1, 0, 0, "#fff3c4", 0, -1.15, 0]],
  guirlande: [...[...Array(9)].map((_, k) => ["s", .07, 0, 0, ["#c8302c", "#e6c21f", "#3f8f45", "#2f5fae"][k % 4], -1.2 + k * .3, -.25 - Math.sin(k / 8 * Math.PI) * .35, 0])],
  fruits: [["c", .4, .3, .2, "#a8723f", 0, .75, 0], ["b", .6, .65, .6, "#e8dcc6", 0, .33, 0], ["s", .12, 0, 0, "#e57a1e", -.12, .92, 0], ["s", .12, 0, 0, "#c8302c", .12, .92, .05], ["s", .11, 0, 0, "#e6c21f", 0, 1.0, -.05]],
  frigo: [["b", .9, 2.0, .7, "#e9eef0", 0, 1.0, 0], ["b", .88, .02, .02, "#9aa5aa", 0, 1.3, .36], ["b", .04, .4, .04, "#9aa5aa", -.35, 1.6, .37], ["b", .04, .4, .04, "#9aa5aa", -.35, .9, .37], ["b", .15, .15, .01, "#e6c21f", .2, 1.6, .36], ["b", .12, .12, .01, "#c8302c", .1, 1.75, .36]],
  microonde: [["b", 1.6, .9, .6, "#e8dcc6", 0, .45, 0], ["b", .7, .4, .4, "#333", 0, 1.1, 0], ["b", .45, .3, .01, "#556", -.08, 1.1, .2]],
  evier: [["b", 2.0, .9, .6, "#e8dcc6", 0, .45, 0], ["b", 2.1, .05, .65, "#8a7a64", 0, .92, 0], ["b", .7, .03, .45, "#aab4b8", 0, .95, 0], ["c", .03, .03, .35, "#aab4b8", 0, 1.1, -.2], ["c", .02, .02, .2, "#aab4b8", 0, 1.27, -.1, 1.57]],
  poubelle: [["c", .25, .22, .7, "#8c8c8c", 0, .35, 0], ["c", .27, .27, .04, "#555", 0, .72, 0]],
  cuisiniere: [["b", .9, .9, .65, "#f4f1ea", 0, .45, 0], ["b", .7, .4, .01, "#2a211d", 0, .45, .33], ...[[-.2, -.15], [.2, -.15], [-.2, .15], [.2, .15]].map(([x, z]) => ["c", .12, .12, .02, "#2a211d", x, .91, z]), ["c", .2, .2, .2, "#8c8c8c", -.2, 1.02, -.15]],
  lavevaisselle: [["b", 1.2, .7, .9, "#e9eef0", 0, .35, 0], ["b", 1.0, .05, .03, "#9aa5aa", 0, .6, .46]],
  ilot: [["b", 2.2, .7, 1.2, "#3f6273", 0, .35, 0], ["b", 2.3, .05, 1.3, "#e8e2d4", 0, .72, 0]],
  tabourets: [...[-.7, 0, .7].flatMap(x => [["c", .2, .2, .05, "#c8302c", x, .7, 0], ["c", .03, .03, .68, "#555", x, .34, 0], ["c", .18, .18, .02, "#555", x, .02, 0]])],
  hotte: [["k", .6, .5, "#aab4b8", 0, -.9, 0], ["c", .15, .15, .7, "#aab4b8", 0, -.35, 0]],
  casseroles: [["b", 1.4, .03, .03, "#555", 0, -.4, 0], ...[-.5, 0, .5].map((x, k) => ["c", .15 + k * .03, .15 + k * .03, .15, ["#8c8c8c", "#c8302c", "#7a4a2a"][k], x, -.65, 0])],
  lavelinge: [["b", .8, .9, .65, "#f4f1ea", 0, .45, 0], ["c", .25, .25, .05, "#9cc8ec", 0, .42, .33, 1.57], ["t", .27, .03, 0, "#8c8c8c", 0, .42, .34], ["b", .7, .08, .02, "#ccc", 0, .82, .33]],
  sechelinge: [["b", .8, .9, .65, "#e9eef0", 0, .45, 0], ["c", .25, .25, .05, "#3f3f3f", 0, .42, .33, 1.57], ["b", .7, .08, .02, "#2f5fae", 0, .82, .33], ["b", .8, .9, .65, "#f4f1ea", .9, .45, 0]],
  bidons: [["c", .18, .18, .5, "#2f5fae", -.3, .25, 0], ["c", .18, .18, .45, "#e57a1e", .1, .23, 0], ["b", .3, .4, .2, "#3f8f45", .45, .2, 0]],
  panier: [["c", .35, .3, .6, "#c49a63", 0, .3, 0], ["b", .5, .15, .4, "#f4f1ea", 0, .62, 0], ["b", .3, .1, .3, "#2f5fae", .1, .7, .05]],
  chaudiere: [["c", .35, .35, 1.6, "#f4f1ea", 0, 1.2, 0], ["c", .03, .03, .4, "#aab4b8", -.15, .2, 0], ["c", .03, .03, .4, "#c8302c", .15, .2, 0], ["c", .08, .08, .02, "#2a211d", 0, 1.3, .35, 1.57]],
  fer: [["b", 1.6, .04, .45, "#9cc8ec", 0, .6, 0], ["b", .05, .6, .05, "#8c8c8c", -.5, .3, 0, 0, 0, .5], ["b", .05, .6, .05, "#8c8c8c", .5, .3, 0, 0, 0, -.5], ["k", .1, .25, "#c8302c", .4, .67, 0, 0, 0, 1.57]],
  bassine: [["c", .6, .45, .3, "#2f5fae", 0, .15, 0], ["s", .1, 0, 0, "#f4f1ea", .1, .3, .1], ["b", .4, .05, .3, "#e58fb2", -.15, .29, 0]],
  balai: [["c", .025, .025, 1.6, "#c8302c", 0, .05, 0, 0, 0, 1.45], ["b", .25, .1, .5, "#e6c21f", .85, .05, 0]],
  etendoir: [["b", 1.8, .03, .03, "#aab4b8", 0, -.6, -.3], ["b", 1.8, .03, .03, "#aab4b8", 0, -.6, .3], ["c", .01, .01, .6, "#555", -.8, -.3, 0], ["c", .01, .01, .6, "#555", .8, -.3, 0], ["b", .5, .6, .02, "#c8302c", -.4, -.9, -.3], ["b", .5, .5, .02, "#2f5fae", .3, -.85, .3]],
  pinces: [["b", 2.0, .01, .01, "#555", 0, -.4, 0], ...[...Array(7)].map((_, k) => ["b", .05, .15, .04, ["#c8302c", "#e6c21f", "#3f8f45", "#2f5fae"][k % 4], -.9 + k * .3, -.47, 0])],
  aspirateur: [["c", .25, .25, .35, "#c8302c", 0, .18, 0], ["c", .03, .03, 1.1, "#555", .15, .7, 0, 0, 0, -.3]],
  bureau: [["b", 2.0, .06, .8, "#a8723f", 0, .75, 0], ["b", .06, .72, .75, "#5b3a26", -.95, .37, 0], ["b", .06, .72, .75, "#5b3a26", .95, .37, 0], ["b", .7, .45, .04, "#111", 0, 1.05, -.2], ["b", .6, .02, .25, "#555", 0, .79, .1], ["c", .07, .1, .25, "#e6c21f", .7, .9, -.1]],
  imprimante: [["b", 1.0, .8, .5, "#7a4a2a", 0, .4, 0], ["b", .6, .25, .45, "#e9eef0", 0, .92, 0], ["b", .4, .02, .2, "#f4f1ea", 0, 1.06, -.05]],
  globe: [["b", .8, .8, .5, "#5b3a26", 0, .4, 0], ["c", .05, .1, .25, "#c9a24a", 0, .92, 0], ["s", .25, 0, 0, "#2f7fae", 0, 1.25, 0], ["t", .27, .015, 0, "#c9a24a", 0, 1.25, 0, 0, 0, .4]],
  caisson: [["b", .55, .7, .55, "#8c8c8c", 0, .35, 0], ...[.15, .35, .55].map(y => ["b", .3, .03, .02, "#555", 0, y, .28])],
  fauteuilbureau: [["c", .3, .3, .08, "#2a211d", 0, .48, 0], ["b", .5, .6, .08, "#2a211d", 0, .82, -.25], ["c", .03, .03, .4, "#555", 0, .25, 0], ["c", .3, .3, .03, "#555", 0, .03, 0]],
  spots: [["b", 1.4, .05, .05, "#2a211d", 0, -.05, 0], ...[-.5, 0, .5].map(x => ["c", .07, .05, .14, "#2a211d", x, -.15, 0])],
  clim: [["b", 1.2, .3, .25, "#f4f1ea", 0, -.25, 0], ["b", 1.0, .03, .02, "#aab4b8", 0, -.35, .13]],
  lampadaire: [["c", .2, .25, .04, "#2a211d", 0, .02, 0], ["c", .025, .025, 1.6, "#2a211d", 0, .8, 0], ["k", .3, .35, "#f4e4b8", 0, 1.7, 0]],
  valise: [["b", .6, .8, .3, "#c8302c", 0, .4, 0], ["b", .25, .04, .04, "#2a211d", 0, .85, 0]],
  armoire: [["b", 1.6, 2.4, .6, "#8a5a33", 0, 1.2, 0], ["b", .02, 2.2, .02, "#5b3a26", 0, 1.2, .31], ["b", .04, .3, .04, "#c9a24a", -.1, 1.3, .32], ["b", .04, .3, .04, "#c9a24a", .1, 1.3, .32]],
  chevet: [["b", .6, .6, .5, "#a8723f", 0, .3, 0], ["c", .12, .15, .3, "#e8dcc6", 0, .75, 0], ["k", .18, .2, "#f4e4b8", 0, 1.0, 0]],
  tetelit: [["b", 2.0, 1.2, .1, "#6b2d3a", 0, .6, 0], ["b", .7, .25, .3, "#f4f1ea", -.45, .55, .2], ["b", .7, .25, .3, "#f4f1ea", .45, .55, .2]],
  coiffeuse: [["b", 1.2, .75, .5, "#e8dcc6", 0, .37, 0], ["c", .4, .4, .03, "#cfe6ff", 0, 1.15, -.2, 1.57], ["c", .03, .03, .3, "#c9a24a", .3, .87, 0], ["s", .06, 0, 0, "#e58fb2", -.3, .8, 0]],
  commode: [["b", 1.5, 1.0, .55, "#7a4a2a", 0, .5, 0], ...[.25, .55, .85].flatMap(y => [["b", 1.4, .02, .02, "#5b3a26", 0, y + .12, .28], ["s", .04, 0, 0, "#c9a24a", -.35, y, .29], ["s", .04, 0, 0, "#c9a24a", .35, y, .29]])],
  chaussons: [["b", .25, .12, .5, "#e58fb2", -.2, .06, 0], ["b", .25, .12, .5, "#e58fb2", .2, .06, .1], ["s", .08, 0, 0, "#fff", -.2, .14, .2], ["s", .08, 0, 0, "#fff", .2, .14, .3]],
  lit: [["b", 2.2, .35, 2.6, "#7a4a2a", 0, .17, 0], ["b", 2.1, .25, 2.5, "#f4f1ea", 0, .45, 0], ["b", 2.15, .08, 1.6, "#7d4aa3", 0, .6, .45], ["b", .7, .15, .4, "#fff", -.5, .62, -.95], ["b", .7, .15, .4, "#fff", .5, .62, -.95]],
  moustiquaire: [["c", .02, .02, .3, "#ddd", 0, -.15, 0], ["k", .9, 1.3, "#f4f1ea", 0, -1.0, 0]],
  coffre: [["b", 1.2, .6, .6, "#e6c21f", 0, .3, 0], ["b", 1.25, .1, .65, "#c8302c", 0, .65, 0], ["s", .15, 0, 0, "#2f5fae", -.3, .8, 0], ["b", .25, .25, .25, "#3f8f45", .3, .8, 0]],
  ours: [["b", .9, .5, .5, "#e8dcc6", 0, .25, 0], ["s", .25, 0, 0, "#a8723f", 0, .75, 0], ["s", .17, 0, 0, "#a8723f", 0, 1.08, 0], ["s", .07, 0, 0, "#a8723f", -.13, 1.22, 0], ["s", .07, 0, 0, "#a8723f", .13, 1.22, 0], ["s", .03, 0, 0, "#2a211d", 0, 1.06, .16]],
  maisonpoupee: [["b", 1.4, .5, .5, "#e8dcc6", 0, .25, 0], ["b", 1.0, .6, .45, "#e58fb2", 0, .8, 0], ["k", .75, .4, "#c8302c", 0, 1.3, 0, 0, .785], ["b", .2, .2, .01, "#9cc8ec", -.25, .85, .23], ["b", .2, .2, .01, "#9cc8ec", .25, .85, .23]],
  cheval: [["b", .9, .25, .3, "#e57a1e", 0, .6, 0], ["b", .2, .4, .2, "#e57a1e", .45, .85, 0], ["t", .5, .04, 0, "#c8302c", 0, .5, 0, 0, 0, 0], ["b", .05, .25, .25, "#7a4a2a", .55, 1.0, 0]],
  litsup: [["b", 1.0, .25, 2.0, "#5aa0d8", 0, .35, 0], ["b", 1.0, .25, 2.0, "#f2c84b", 0, 1.55, 0], ...[[-.48, -.98], [.48, -.98], [-.48, .98], [.48, .98]].map(([x, z]) => ["b", .06, 2.0, .06, "#f4f1ea", x, 1.0, z]), ["b", .04, 1.4, .04, "#f4f1ea", .3, .9, 1.02], ["b", .04, 1.4, .04, "#f4f1ea", -.1, .9, 1.02]],
  ballon: [["s", .3, 0, 0, "#f4f1ea", 0, .3, 0], ["s", .31, 0, 0, "#2a211d", 0, .3, 0, 0, 0, 0, .25]],
  tapispuzzle: [...[...Array(12)].map((_, k) => ["b", .6, .03, .6, ["#c8302c", "#e6c21f", "#3f8f45", "#2f5fae"][k % 4], -.9 + (k % 4) * .6, .015, -.9 + Math.floor(k / 4) * .6])],
  train: [["b", .5, .35, .35, "#c8302c", -.7, .2, 0], ["c", .08, .08, .2, "#2a211d", -.6, .45, 0], ["b", .45, .25, .3, "#2f5fae", -.15, .15, 0], ["b", .45, .25, .3, "#3f8f45", .35, .15, 0], ["b", 2.0, .02, .15, "#8c8c8c", 0, .01, 0]],
  mobile: [["c", .01, .01, .5, "#555", 0, -.25, 0], ["b", 1.0, .02, .02, "#c9a24a", 0, -.5, 0], ["s", .1, 0, 0, "#e6c21f", -.45, -.75, 0], ["s", .1, 0, 0, "#c8302c", .45, -.8, 0], ["k", .1, .2, "#3f8f45", 0, -.75, 0]],
  etoiles: [...[...Array(8)].map((_, k) => ["s", .08, 0, 0, "#f2c84b", Math.cos(k * 2.4) * 1.1, -.05, Math.sin(k * 2.4) * .8])],
  trottinette: [["b", .2, .04, .9, "#5aa0d8", 0, .12, 0], ["c", .02, .02, .9, "#5aa0d8", 0, .6, .4], ["b", .5, .03, .03, "#2a211d", 0, 1.05, .4], ["c", .08, .08, .05, "#2a211d", 0, .08, .45, 0, 0, 1.57], ["c", .08, .08, .05, "#2a211d", 0, .08, -.45, 0, 0, 1.57]],
  baignoire: [["b", 2.4, .6, .9, "#f4f1ea", 0, .3, 0], ["b", 2.2, .02, .7, "#8fcbe0", 0, .58, 0], ["s", .1, 0, 0, "#e6c21f", .4, .62, .1], ["c", .03, .03, .3, "#aab4b8", -1.0, .75, -.35]],
  radiateur: [["b", 1.0, .9, .1, "#f4f1ea", 0, .55, 0], ["b", .9, .5, .03, "#e57a1e", 0, .65, .07], ["b", .9, .3, .03, "#2f5fae", 0, .3, .07]],
  lavabo: [["b", 1.0, .75, .5, "#e8dcc6", 0, .37, 0], ["c", .3, .22, .15, "#f4f1ea", 0, .82, 0], ["c", .02, .02, .2, "#aab4b8", 0, .95, -.18]],
  verre: [["b", .8, .8, .4, "#e8dcc6", 0, .4, 0], ["c", .08, .07, .2, "#9cc8ec", 0, .9, 0], ["c", .015, .015, .3, "#c8302c", .03, 1.05, 0, 0, 0, .2], ["c", .015, .015, .3, "#2f5fae", -.03, 1.05, 0, 0, 0, -.2]],
  douche: [["b", 1.1, .1, 1.1, "#f4f1ea", 0, .05, 0], ["c", .02, .02, 2.1, "#aab4b8", -.4, 1.1, -.4], ["c", .15, .15, .04, "#aab4b8", -.2, 2.15, -.4], ["b", .02, 2.0, 1.1, "#cfe6ff", .55, 1.05, 0]],
  balance: [["b", .5, .06, .5, "#f4f1ea", 0, .03, 0], ["b", .2, .01, .1, "#2a211d", 0, .065, -.1]],
  tapisbain: [["b", 1.4, .03, .9, "#5aa0d8", 0, .015, 0], ["b", 1.2, .035, .7, "#f4f1ea", 0, .017, 0]],
  neon: [["b", 1.6, .08, .15, "#f4f1ea", 0, -.05, 0], ["c", .03, .03, 1.5, "#fffbe8", 0, -.12, 0, 0, 0, 1.57]],
  rideaudouche: [["c", .02, .02, 1.6, "#aab4b8", 0, -.2, 0, 0, 0, 1.57], ...[...Array(6)].map((_, k) => ["b", .26, 1.1, .02, k % 2 ? "#f4f1ea" : "#5aa0d8", -.65 + k * .26, -.8, (k % 2) * .05])],
  wc: [["c", .25, .2, .4, "#f4f1ea", 0, .2, .1], ["c", .27, .27, .05, "#f4f1ea", 0, .42, .1], ["b", .5, .5, .2, "#f4f1ea", 0, .6, -.2]],
  papier: [["c", .02, .02, .3, "#c9a24a", 0, .75, 0, 0, 0, 1.57], ["c", .1, .1, .12, "#fff", 0, .75, .05, 0, 0, 1.57], ["c", .1, .1, .12, "#fff", .35, .1, 0]],
  chasse: [["b", .5, .7, .2, "#f4f1ea", 0, .95, 0], ["b", .2, .12, .02, "#aab4b8", 0, 1.1, .11]],
  balayette: [["c", .12, .1, .4, "#3f8f45", 0, .2, 0], ["c", .02, .02, .5, "#2a211d", 0, .5, 0]],
  magazines: [["b", .5, .5, .4, "#a8723f", 0, .25, 0], ["b", .4, .05, .3, "#c8302c", 0, .53, 0], ["b", .4, .05, .3, "#2f5fae", .05, .58, 0, 0, .3]],
  spray: [["c", .07, .07, .3, "#7d4aa3", 0, .15, 0], ["c", .03, .03, .06, "#fff", 0, .33, 0]],
  ampoule: [["c", .01, .01, .6, "#2a211d", 0, -.3, 0], ["s", .12, 0, 0, "#fff3c4", 0, -.68, 0]],
  lucarne: [["b", 1.0, .03, .8, "#9cc8ec", 0, -.02, 0], ["b", 1.1, .05, .9, "#f4f1ea", 0, -.01, 0]],
  malle: [["b", 1.4, .7, .7, "#5b3a26", 0, .35, 0], ["c", .35, .35, 1.4, "#6e4a2c", 0, .7, 0, 0, 0, 1.57], ["b", .06, .75, .72, "#c9a24a", -.4, .38, 0], ["b", .06, .75, .72, "#c9a24a", .4, .38, 0]],
  mannequin: [["c", .25, .3, .05, "#2a211d", 0, .03, 0], ["c", .02, .02, 1.0, "#2a211d", 0, .5, 0], ["c", .25, .2, .7, "#e8dcc6", 0, 1.35, 0], ["s", .2, 0, 0, "#e8dcc6", 0, 1.6, 0], ["c", .05, .05, .15, "#e8dcc6", 0, 1.78, 0]],
  gramo: [["b", .5, .25, .5, "#7a4a2a", 0, .12, 0], ["c", .2, .2, .02, "#2a211d", 0, .26, 0], ["k", .3, .6, "#c9a24a", .1, .55, -.1, 0, 0, -2.4]],
  rouleau: [["c", .22, .22, 2.4, "#8e1c22", 0, .22, 0, 0, 0, 1.57]],
  poupee: [["b", .8, .4, .5, "#e8dcc6", 0, .2, 0], ["k", .2, .4, "#e58fb2", 0, .6, 0], ["s", .12, 0, 0, "#f6d7b8", 0, .9, 0], ["s", .13, 0, 0, "#e6c21f", 0, .95, -.03]],
  poutre: [["b", 3.0, .3, .3, "#4a3020", 0, -.15, 0], ["b", .25, .25, 1.2, "#4a3020", -1.2, -.4, 0, .7]],
  toile: [...[0, .785, 1.57, 2.356].map(a => ["b", 1.2, .005, .005, "#ddd", 0, -.05, 0, 0, a]), ["t", .3, .005, 0, "#ddd", 0, -.05, 0, 1.57], ["t", .5, .005, 0, "#ddd", 0, -.05, 0, 1.57], ["s", .06, 0, 0, "#2a211d", .2, -.4, .1]],
  velo: [["t", .35, .04, 0, "#2a211d", -.55, .37, 0], ["t", .35, .04, 0, "#2a211d", .55, .37, 0], ["b", 1.0, .05, .05, "#c8302c", 0, .65, 0, 0, 0, .1], ["c", .02, .02, .5, "#c8302c", .4, .6, 0, 0, 0, .3], ["b", .25, .05, .1, "#2a211d", -.3, .95, 0]],
  vins: [["b", 1.4, 2.0, .4, "#5b3a26", 0, 1.0, 0], ...[...Array(15)].map((_, k) => ["c", .07, .07, .3, "#2a3f20", -.5 + (k % 5) * .25, .4 + Math.floor(k / 5) * .55, .1, 1.57])],
  tonneau: [["c", .45, .45, .9, "#7a4a2a", 0, .45, 0, 0, 0, 1.57], ["t", .46, .02, 0, "#2a211d", -.3, .45, 0, 0, 1.57], ["t", .46, .02, 0, "#2a211d", .3, .45, 0, 0, 1.57], ["b", .5, .03, .03, "#c9a24a", 0, .1, .4]],
  seau: [["c", .22, .17, .35, "#aab4b8", 0, .17, 0], ["t", .2, .01, 0, "#555", 0, .42, 0]],
  etagere: [["b", 1.6, 2.2, .45, "#8c8c8c", 0, 1.1, 0], ...[.5, 1.0, 1.5, 2.0].map(y => ["b", 1.55, .03, .44, "#aab4b8", 0, y, 0]), ["b", .4, .3, .3, "#c49a63", -.4, .67, 0], ["c", .1, .1, .35, "#3f8f45", .3, 1.2, 0], ["b", .6, .3, .3, "#c49a63", 0, 1.67, 0]],
  cagette: [["b", .8, .3, .5, "#c49a63", 0, .15, 0], ...[...Array(6)].map((_, k) => ["s", .1, 0, 0, k % 2 ? "#c8302c" : "#3f8f45", -.25 + (k % 3) * .25, .32, -.1 + Math.floor(k / 3) * .2])],
  tapette: [["b", .4, .03, .2, "#c49a63", 0, .015, 0], ["b", .35, .02, .02, "#aab4b8", 0, .05, 0], ["b", .08, .06, .05, "#e6c21f", .12, .05, 0]],
  jambon: [["c", .01, .01, .5, "#c49a63", 0, -.25, 0], ["k", .2, .6, "#8e1c22", 0, -.8, 0, 3.14], ["c", .02, .02, .5, "#c49a63", .5, -.25, 0], ["c", .1, .08, .5, "#c9a24a", .5, -.75, 0]],
  outils: [["b", 2.0, 1.2, .05, "#c49a63", 0, .9, 0], ["b", .05, .5, .05, "#c8302c", -.6, .9, .05], ["b", .3, .1, .05, "#555", -.6, 1.15, .05], ["b", .05, .6, .05, "#2f5fae", 0, .9, .05], ["t", .15, .03, 0, "#555", .5, 1.0, .05], ["b", 2.0, .8, .5, "#8c8c8c", 0, .4, .2]],
  bidon: [["b", .4, .5, .25, "#c8302c", 0, .25, 0], ["c", .04, .04, .1, "#2a211d", .12, .55, 0]],
  portegarage: [["b", 2.2, 2.2, .08, "#d9d9d9", 0, 1.1, 0], ...[...Array(8)].map((_, k) => ["b", 2.2, .02, .1, "#aaa", 0, .2 + k * .27, .02])],
  escabeau: [["b", .5, 1.4, .05, "#aab4b8", 0, .7, -.25, -.2], ["b", .5, 1.4, .05, "#aab4b8", 0, .7, .25, .2], ...[.3, .6, .9].map(y => ["b", .45, .03, .2, "#aab4b8", 0, y, .2 - y * .15])],
  voiture: [["b", 1.7, .6, 3.4, "#c8302c", 0, .5, 0], ["b", 1.5, .5, 1.8, "#9cc8ec", 0, 1.05, -.2], ...[[-.8, -1.1], [.8, -1.1], [-.8, 1.1], [.8, 1.1]].map(([x, z]) => ["c", .32, .32, .25, "#2a211d", x, .32, z, 0, 0, 1.57]), ["b", .3, .12, .02, "#fff3c4", -.55, .6, 1.71], ["b", .3, .12, .02, "#fff3c4", .55, .6, 1.71]],
  caisse: [["b", .8, .35, .4, "#c8302c", 0, .17, 0], ["b", .5, .05, .05, "#2a211d", 0, .45, 0]],
  etabli: [["b", 1.8, .1, .8, "#a8723f", 0, .7, 0], ["b", .1, .65, .7, "#5b3a26", -.8, .33, 0], ["b", .1, .65, .7, "#5b3a26", .8, .33, 0], ["b", .5, .2, .25, "#555", .2, .85, 0]],
  pneus: [["t", .4, .15, 0, "#2a211d", 0, .15, 0, 1.57], ["t", .4, .15, 0, "#2a211d", 0, .45, 0, 1.57]],
  velosusp: [["c", .01, .01, .4, "#555", -.5, -.2, 0], ["c", .01, .01, .4, "#555", .5, -.2, 0], ["t", .35, .04, 0, "#2a211d", -.55, -.75, 0], ["t", .35, .04, 0, "#2a211d", .55, -.75, 0], ["b", 1.0, .05, .05, "#2f5fae", 0, -.5, 0]],
  haie: [["b", 2.4, 1.0, .7, "#3f6f2e", 0, .5, 0], ...[-.9, -.3, .3, .9].map(x => ["s", .4, 0, 0, "#4a8034", x, 1.0, 0])],
  niche: [["b", 1.0, .7, .9, "#c8302c", 0, .35, 0], ["k", .8, .45, "#7a4a2a", 0, .95, 0, 0, .785], ["b", .4, .45, .02, "#2a211d", 0, .3, .46]],
  arbre: [["c", .18, .25, 1.4, "#6e4a2c", 0, .7, 0], ["s", .9, 0, 0, "#3f8f45", 0, 1.9, 0], ["s", .6, 0, 0, "#4d9f52", .5, 2.2, .2], ["s", .1, 0, 0, "#c8302c", .4, 1.6, .7], ["s", .1, 0, 0, "#c8302c", -.5, 1.9, .6]],
  nain: [["b", .8, .4, .5, "#9b8f80", 0, .2, 0], ["c", .18, .2, .35, "#2f5fae", 0, .58, 0], ["s", .14, 0, 0, "#f6d7b8", 0, .85, 0], ["k", .14, .35, "#c8302c", 0, 1.1, 0], ["k", .12, .2, "#f4f1ea", 0, .76, .08, 3.14]],
  bbq: [["c", .4, .3, .35, "#2a211d", 0, .85, 0], ...[0, 2.1, 4.2].map(a => ["c", .025, .025, .8, "#2a211d", Math.cos(a) * .25, .38, Math.sin(a) * .25]), ["s", .08, 0, 0, "#c8302c", 0, 1.05, 0]],
  fleurs: [["b", 2.4, .25, 2.4, "#6e4a2c", 0, .12, 0], ...[...Array(16)].map((_, k) => ["s", .13, 0, 0, ["#c8302c", "#e6c21f", "#e58fb2", "#7d4aa3"][k % 4], -.9 + (k % 4) * .6, .35, -.9 + Math.floor(k / 4) * .6])],
  tablejardin: [["c", .8, .8, .05, "#f4f1ea", 0, .7, 0], ["c", .05, .05, .7, "#f4f1ea", 0, .35, 0], ["c", .03, .03, 2.0, "#c49a63", 0, .95, 0]],
  brouette: [["b", .7, .3, 1.0, "#3f8f45", 0, .45, 0], ["c", .2, .2, .08, "#2a211d", 0, .2, .6, 0, 0, 1.57], ["c", .02, .02, .9, "#555", -.25, .4, -.6, 1.3], ["c", .02, .02, .9, "#555", .25, .4, -.6, 1.3]],
  soleil: [["s", .45, 0, 0, "#f2c84b", 0, -.6, 0], ...[...Array(8)].map((_, k) => ["b", .08, .5, .02, "#f2c84b", Math.cos(k * .785) * .75, -.6 + Math.sin(k * .785) * .75, 0, 0, 0, k * .785 + 1.57])],
  nuage: [["s", .4, 0, 0, "#ffffff", 0, -.5, 0], ["s", .3, 0, 0, "#ffffff", .45, -.55, 0], ["s", .32, 0, 0, "#ffffff", -.45, -.55, 0], ["s", .25, 0, 0, "#ffffff", .2, -.3, 0]],
  arrosoir: [["c", .22, .25, .45, "#3f8f45", 0, .23, 0], ["c", .03, .05, .5, "#3f8f45", .3, .4, 0, 0, 0, -.9], ["t", .15, .02, 0, "#3f8f45", -.05, .5, 0]],
  serviette: [["b", .8, .9, .05, "#e57a1e", 0, .9, 0], ["b", .8, .15, .05, "#f4f1ea", 0, .7, .01], ["b", .06, 1.3, .06, "#aab4b8", -.45, .65, 0], ["b", .06, 1.3, .06, "#aab4b8", .45, .65, 0]],
  plongeoir: [["b", .6, .5, .6, "#f4f1ea", 0, .25, 0], ["b", .5, .05, 1.8, "#2f5fae", 0, .55, .6]],
  bouee: [["t", .4, .14, 0, "#c8302c", 0, .9, 0], ["t", .41, .145, 0, "#f4f1ea", 0, .9, 0, 0, 0, .785]],
  transat: [["b", .7, .1, 1.6, "#f4f1ea", 0, .35, .2], ["b", .7, .8, .08, "#2f5fae", 0, .7, -.55, -.5], ["c", .03, .03, .35, "#aab4b8", -.3, .17, .8], ["c", .03, .03, .35, "#aab4b8", .3, .17, .8]],
  matelas: [["b", 1.0, .2, 2.2, "#e6c21f", 0, .1, 0], ["b", 1.0, .25, .4, "#e57a1e", 0, .13, -.9]],
  bassin: [["b", 3.0, .06, 3.6, "#2f8fbf", 0, .02, 0], ["b", 3.2, .05, .15, "#f4f1ea", 0, .03, 1.85], ["b", 3.2, .05, .15, "#f4f1ea", 0, .03, -1.85]],
  echelle: [["t", .3, .03, 0, "#aab4b8", -.3, .5, 0, 0, 1.57, 0], ["t", .3, .03, 0, "#aab4b8", .3, .5, 0, 0, 1.57, 0], ...[.15, .35].map(y => ["b", .6, .03, .1, "#aab4b8", 0, y, .25])],
  parasol: [["c", .03, .03, 1.0, "#f4f1ea", 0, -.5, 0], ["k", 1.2, .4, "#c8302c", 0, -1.1, 0], ["k", 1.21, .39, "#f4f1ea", 0, -1.1, 0, 0, .4]],
  oiseau: [["s", .12, 0, 0, "#f4f1ea", 0, -.5, 0], ["b", .7, .02, .15, "#f4f1ea", 0, -.48, 0, 0, 0, .25], ["k", .04, .1, "#e6c21f", 0, -.5, .15, 1.57]],
  citronnier: [["c", .35, .28, .5, "#b9603d", 0, .25, 0], ["c", .05, .05, .6, "#6e4a2c", 0, .8, 0], ["s", .5, 0, 0, "#3f8f45", 0, 1.3, 0], ...[[.3, 1.2, .3], [-.3, 1.4, .2], [0, 1.1, .45]].map(([x, y, z]) => ["s", .08, 0, 0, "#f2d33b", x, y, z])],
  hamac: [["c", .03, .03, 1.2, "#7a4a2a", -1.1, .6, 0], ["c", .03, .03, 1.2, "#7a4a2a", 1.1, .6, 0], ["b", 1.9, .05, .7, "#e57a1e", 0, .55, 0]],
  rambarde: [["b", 2.4, .06, .08, "#2a211d", 0, 1.0, 0], ...[...Array(9)].map((_, k) => ["b", .03, 1.0, .03, "#2a211d", -1.1 + k * .275, .5, 0])],
  lanterne: [["b", .3, .45, .3, "#2a211d", 0, .7, 0], ["b", .22, .35, .32, "#fff3c4", 0, .7, 0], ["b", .7, .45, .5, "#7a4a2a", 0, .22, 0]],
  balancelle: [["b", 1.8, .1, .6, "#f4f1ea", 0, .5, 0], ["b", 1.8, .6, .08, "#f4f1ea", 0, .8, -.27], ["c", .02, .02, 1.0, "#555", -.85, 1.2, 0], ["c", .02, .02, 1.0, "#555", .85, 1.2, 0], ["b", 2.0, .06, .06, "#555", 0, 1.7, 0]],
  coussins: [["b", .7, .2, .7, "#e57a1e", -.5, .1, 0], ["b", .7, .2, .7, "#2f5fae", .4, .1, .2], ["b", .6, .2, .6, "#e6c21f", 0, .3, -.1, 0, .4]],
  store: [["b", 2.4, .05, 1.4, "#c8302c", 0, -.3, .3, .25], ...[...Array(6)].map((_, k) => ["b", .2, .055, 1.4, "#f4f1ea", -1.0 + k * .4, -.3, .3, .25])],
  lune: [["s", .4, 0, 0, "#f4f1ea", 0, -.6, 0], ["s", .35, 0, 0, "#f4c58a", .2, -.55, .12]]
};
function furn(kind) {
  const g = new THREE.Group(), spec = FURN[kind]; if (!spec) return g;
  for (const [t, a, b, c, col, x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0] of spec) {
    const geo = t === "b" ? new THREE.BoxGeometry(a, b, c) : t === "c" ? new THREE.CylinderGeometry(a, b, c, 18) : t === "s" ? new THREE.SphereGeometry(a, 14, 10)
      : t === "k" ? new THREE.ConeGeometry(a, b, 18) : new THREE.TorusGeometry(a, b, 8, 22);
    const m = new THREE.Mesh(geo, mat({ color: col })); m.position.set(x, y, z); m.rotation.set(rx, ry, rz); g.add(m);
  }
  return g;
}
function lisaFurnish(ri, g) {   // un objet par surface, posé près de son panneau
  const r = R[ri], H = r.home;
  H.o.forEach(([lab, kind, mode], i) => {
    const p = panelSpec(i), o = furn(kind), n = p.u.clone().cross(p.v).normalize(), bb = new THREE.Box3().setFromObject(o), sz = bb.getSize(V3(0, 0, 0));
    if (i <= 4) {   // murs : objet bas sous le panneau, ou objet haut à côté (côté entrée sur les murs latéraux)
      const side = mode === "T" && i !== 1 && i !== 3, dir = p.u.z > 0 ? p.u.clone() : p.u.clone().negate();
      const pos = V3(p.c.x, 0, p.c.z).addScaledVector(n, sz.z / 2 + .05);
      if (side) pos.addScaledVector(i === 2 ? p.u : dir, 1.3 + sz.x / 2 + .1);
      o.position.copy(pos); o.rotation.y = Math.atan2(n.x, n.z);
      addBox(ri, pos.x, pos.z, Math.max(sz.x, sz.z) / 2 * .8);
    } else if (i <= 7) { o.position.set(p.c.x, 0, p.c.z); addBox(ri, p.c.x, p.c.z, 1.15); }   // sol : l'objet sert de socle au pupitre
    else { o.position.set(p.c.x, H.out ? H_ROOM : H_ROOM, p.c.z + 2.1); }   // plafond : suspendu devant le panneau
    g.add(o);
  });
  const lm = furn(H.land); lm.position.set(-4.4, 0, 4.1); lm.rotation.y = Math.PI / 4; g.add(lm); addBox(ri, -4.4, 4.1, .7);
}
