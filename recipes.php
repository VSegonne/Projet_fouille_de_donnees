<?php

require_once './vendor/autoload.php';
include_once('vendor/simplehtmldom_1_5/simple_html_dom.php');

use sylouuu\MarmitonCrawler\Recipe\Recipe;

$recipes = array();

function get_links($url) {

	global $recipes;
	$input = @file_get_contents($url);
	$regexp = "<a\s[^>]*href=(\"??)([^\" >]*?)\\1[^>]*>(.*)<\/a>";
	preg_match_all("/$regexp/siU",$input,$matches);
	$base_url = parse_url($url,PHP_URL_HOST);

	$l = $matches[2];
	foreach ($l as $link) {

		if (strpos($link, "#")) {
			$link = substr($link,0,strpos($link,"#"));
		}
		if (substr($link,0,1) == ".") {
			$link = substr($link,1);
		}

		if (substr($link,0,7) == "http://") {
			$link = $link ;
		} else if (substr($link,0,8) == "https://") {
			$link = $link;
		} else if (substr($link,0,2) == "//") {
			$link = substr($link,2);
		} else if (substr($link,0,1) == "#") {
			$link = $url;
		} else if (substr($link,0,7) == "mailto:") {
			$link = "[".$link."]";
		} 

		if (substr($link,0,1) == "'") {
			$link = substr($link,1,strlen($link)-1);
		}
		if (substr($link,-1) == "'") {
			$link = substr($link,0,strlen($link)-1);
		}

		if (substr($link,0,1) == "/") {
			$link = $base_url.$link;
		}

		if (substr($link,0,7) != "http://" && substr($link,0,8) != "https://" && substr($link,0,1) != "[") {
			if (substr($url,0,8) == "https://") {
				$link = "https://".$link;
			} else {
				$link = "http://".$link;
			}
		}

		if (!in_array($link, $recipes) && preg_match('/recettes\/recette_/', $link)) {
			array_push($recipes, $link);
		}
	}

	return $recipes;

}

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

# ======
#  MAIN
# ======


$to_crawl = "http://www.marmiton.org/recettes/recette-hasard.aspx";
$file = fopen('sorties_02132016.txt', 'a');

foreach (get_links($to_crawl) as $page) {
	$recipe = new Recipe($page);
	$recipe = $recipe -> getRecipe();
	var_dump($recipe);
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
	foreach (fetch_ingredients($page) as $ing) {
		fwrite($file, "ingredient\t");
		fwrite($file, $ing."\n");
	}
	fwrite($file,"instructions\t");
	foreach (explode("\n", $recipe["instructions"]) as $s) {
		fwrite($file, trim($s)." ");
	}
	fwrite($file, "\n\n");

}

fclose($file);

/*
$page = 'http://www.marmiton.org/recettes/recette_gratin-de-pommes-granny-au-chevre_37910.aspx';
$recipe = new Recipe($page);
$recipe = $recipe -> getRecipe();
var_dump($recipe);

$file = fopen('output.txt', 'a');

fwrite($file,"recipe_name\t");
fwrite($file, $recipe["recipe_name"]."\n");
fwrite($file,"type\t");
fwrite($file, $recipe["type"]."\n");
fwrite($file,"difficulty\t");
fwrite($file, $recipe["difficulty"]."\n");
fwrite($file,"cost\t");
fwrite($file, $recipe["cost"]."\n");
fwrite($file,"guests_number\t");
fwrite($file, strval($recipe["guests_number"])."\n");
fwrite($file,"preparation_time\t");
fwrite($file, $recipe["preparation_time"]."\n");
fwrite($file,"cook_time\t");
fwrite($file, $recipe["cook_time"]."\n");
foreach (fetch_ingredients($page) as $ing) {
	fwrite($file,"ingredient\t");
	fwrite($file, $ing."\n");
}
fwrite($file,"instructions\t");
foreach (explode("\n", $recipe["instructions"]) as $s) {
	fwrite($file, trim($s)." ");
}
fwrite($file, "\n\n");

fclose($file);
*/

?>
