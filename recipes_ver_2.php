<?php

require_once './vendor/autoload.php';
include_once('vendor/simplehtmldom_1_5/simple_html_dom.php');

use sylouuu\MarmitonCrawler\Recipe\Recipe;

# $html = http://www.marmiton.org/recettes/recettes-index.aspx
#function fetch_letters ($html) {
#	$html = file_get_html($html);
#	$rs = $html->find('div');
#}


function fetch_ingredients ($html) {
  $html = file_get_html($html);
  $ret = $html->find('script[type="text/javascript"]');
  foreach ($ret as $r) {
    if (substr($r,0,46) == "<script type=\"text/javascript\">var m_dataLayer") {
      $r = preg_replace('/\s+/', '', $r);
      return explode(",",explode("\",\"recipeType\"",explode("\"contentInfo\":{\"recipeIngredients\":\"",explode(';',$r)[0])[1])[0]);
    }
  }
}

function fetch_recipes ($html) {
	$recipes = array();
	$html = file_get_html($html);
	$rs = $html->find('div[class="content"] ul.m-lsting-recipe');
	foreach ($rs as $r) {
		$r = $r->find('li a');
		foreach ($r as $a) {
			array_push($recipes,$a->href);
		}
	}
	return $recipes;
}

function write_recipe($page) {

	

	echo $page."\n";

	$recipe = new Recipe($page);
	$recipe = $recipe -> getRecipe();

	if (count($recipe)!= 0) {
		$file = fopen('recipes_index_A.txt', 'a');
		fwrite($file,"url\t");
		fwrite($file, $page."\n");
		fwrite($file,"recipe_name\t");
		fwrite($file, $recipe["recipe_name"]."\n");
		fwrite($file,"type\t");
		fwrite($file, $recipe["type"]."\n");
		fwrite($file,"difficulty\t");
		fwrite($file, $recipe["difficulty"]."\n");
		fwrite($file,"cost\t");
		fwrite($file, $recipe["cost"]."\n");
		fwrite($file,"guests_number\t");
		fwrite($file, $recipe["guests_number"]."\n");
		fwrite($file,"preparation_time\t");
		fwrite($file, $recipe["preparation_time"]."\n");
		fwrite($file,"cook_time\t");
		fwrite($file, $recipe["cook_time"]."\n");
		fwrite($file, "ingredients\t");
		$a = fetch_ingredients($page);
		for ($i=0; $i<count($a)-1; $i++) { 
			fwrite($file, $a[$i]."|");
		}
		fwrite($file, $a[count($a)-1]);
		fwrite($file, "\n");
		fwrite($file,"instructions\t");
		foreach (explode("\n", $recipe["instructions"]) as $s) {
			fwrite($file,str_replace("?","'", trim($s))." ");
		}
		fwrite($file, "\n\n");
		fclose($file);
	}
}

# ======
#  MAIN
# ======


$crawled_recipes = array();

$list_ing = array('abadeche','abondance','abricot','absinthe','achatine','acide-citrique','acide-lactique','acide-tartrique','acidifiant','acoupa','adjwain','after-eight','agar-agar','agneau','agrume-confit','aiguillette-de-canard','aiguillette-de-poulet','aiguillettes-de-dinde','ail','ail-semoule','aile-de-poulet','aillet','aioli','airelles','alcool-de-poire','alevin','alfafa','algue-dulse','algue-japonaise','algue-sechee','alkermes','all-bran','alose','alouette','amande','amarante','amaretti','amaretto','amidon','ananas','anchoiade','anchois','andouille','andouillette','aneth','angelique','angostura','anguille','anis','anis-en-poudre','anis-etoile','anisette','anti-pectine','apericube','aperifruit','appenzeller','arachide','araignee-de-mer','arbouse','armagnac','armoise','aromate','arome','arome-amande-amere','arome-citron','arome-fleur-d-oranger','arome-maggi','arome-vanille','arquebuse','arrow-root','artichaut','artichaut-violet','asafoetida','asiago','aspartame','asperge','asperule','asti-spumante','atriau','attieke','aubergine','autruche','avocat','avoine');

foreach ($list_ing as $ing) {
	$list_search = array("http://www.marmiton.org/recettes/recettes-index.aspx?ingredient=".$ing,
	"http://www.marmiton.org/recettes/recettes-index.aspx?ingredient=".$ing."&page=2",
	"http://www.marmiton.org/recettes/recettes-index.aspx?ingredient=".$ing."&page=3",
	"http://www.marmiton.org/recettes/recettes-index.aspx?ingredient=".$ing."&page=4",
	"http://www.marmiton.org/recettes/recettes-index.aspx?ingredient=".$ing."&page=5",
	"http://www.marmiton.org/recettes/recettes-index.aspx?ingredient=".$ing."&page=6",
	"http://www.marmiton.org/recettes/recettes-index.aspx?ingredient=".$ing."&page=7",
	"http://www.marmiton.org/recettes/recettes-index.aspx?ingredient=".$ing."&page=8",
	"http://www.marmiton.org/recettes/recettes-index.aspx?ingredient=".$ing."&page=9",
	"http://www.marmiton.org/recettes/recettes-index.aspx?ingredient=".$ing."&page=10"
	);

	foreach ($list_search as $html) {
		foreach (fetch_recipes($html) as $page) {
			if (substr($page,0,18) == "/recettes/recette_") {
				$code = hash("md5",$page,false);
				if (! in_array($code, $crawled_recipes)) {
					write_recipe("http://www.marmiton.org".$page);
					array_push($crawled_recipes,$code);
				}
			}
		}
	}
}


#write_recipe("http://www.marmiton.org/recettes/recette_tartilla-aux-abricots_313409.aspx");

?>
