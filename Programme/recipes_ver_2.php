<?php

require_once './vendor/autoload.php';
include_once('vendor/simplehtmldom_1_5/simple_html_dom.php');

use sylouuu\MarmitonCrawler\Recipe\Recipe;

function cost ($html) {
	$html = file_get_html($html);
	$r = $html->find('div.m_content_recette_breadcrumb');
	return explode(" - ",trim($r[0]->plaintext))[1]."\n";
}

function fetch_letters ($html) {
	/*
		input : "html = http://www.marmiton.org/recettes/recettes-index.aspx"
		output : ["http://www.marmiton.org/recettes/recettes-index.aspx?letter=A",
		          "http://www.marmiton.org/recettes/recettes-index.aspx?letter=B",
		          ...]
	*/
	$queries = array();
	$html = file_get_html($html);
	$rs = $html->find('div.m-lst-page ul li a');
	foreach ($rs as $r) {
		array_push($queries,"http://www.marmiton.org".$r->href);
	}
	return $queries;
}

function fetch_ingredients ($html) {
	/*
		input : "http://www.marmiton.org/recettes/recettes-index.aspx?letter=A"
		output : ["http://www.marmiton.org/recettes/recettes-index.aspx?ingredient=abadeche",
                  "http://www.marmiton.org/recettes/recettes-index.aspx?ingredient=abondance",
                  ...]
	*/
	$ingres = array();
	$html = file_get_html($html);
	$rs = $html->find('div.content ul.m-lsting-ing li a');
	foreach ($rs as $r) {
		array_push($ingres,"http://www.marmiton.org".$r->href);
	}
	return $ingres;
}

function fetch_pages ($html) {
	/*
		input : "http://www.marmiton.org/recettes/recettes-index.aspx?ingredient=abadeche"
		output : []
		inpout : "http://www.marmiton.org/recettes/recettes-index.aspx?ingredient=lait"
		output : ["http://www.marmiton.org/recettes/recettes-index.aspx?ingredient=lait&page=1",
                  "http://www.marmiton.org/recettes/recettes-index.aspx?ingredient=lait&page=2",
                  ...]
	*/
	$pages = array();
	$html = file_get_html($html);
	$rs = $html->find('div.m_bloc_cadre div.content div.ToCPagingContainer a');
	foreach ($rs as $r) {
		array_push($pages,"http://www.marmiton.org".$r->href);
	}
	return $pages;
}

function fetch_recipes ($html) {
	/*
		fonction qui une liste d'urls (/recettes/recette_)
		niveau = une page des résultats d'une requete
	*/
	$recipes = array();
	$html = file_get_html($html);
	$rs = $html->find('div.content ul.m-lsting-recipe li a');
	foreach ($rs as $r) {
		array_push($recipes,"http://www.marmiton.org".$r->href);
	}
	return $recipes;
}

function fetch_all ($file,$html) {

	$bd = array();

	#while (count($bd) <= 10000) {

		#foreach (fetch_letters($html) as $letter) {
			foreach (fetch_ingredients("http://www.marmiton.org/recettes/recettes-index.aspx?letter=B") as $ingredient) {
				echo "page ingre : ".$ingredient."\n";
				if (count(fetch_pages($ingredient)) == 0) {
					foreach (fetch_recipes($ingredient) as $recipe) {
						if (!in_array($recipe,$bd) and substr($recipe,0,41) == "http://www.marmiton.org/recettes/recette_") {
							array_push($bd,$recipe);
							#echo $recipe."\n";
							write_recipe($file,$recipe);
						}
					}
				} else {
					echo "N-pages"."\n";
					foreach (fetch_pages($ingredient) as $page) {
						foreach (fetch_recipes($page) as $recipe) {
							if (!in_array($recipe,$bd) and substr($recipe,0,41) == "http://www.marmiton.org/recettes/recette_") {
								array_push($bd,$recipe);
								#echo $recipe."\n";
								write_recipe($file,$recipe);
							}
						}
					}
				}
				echo "#recipes = ".count($bd)."\n";
			}
		#}

	#}
}

# ==================
# === SEPARATOR ====
# ==================

function write_ingredients ($html) {
	/*
		fonction utilisée dans l'écriture d'une recette
		forme d'écriture d'ingredients du package Marmitoncrawler est rejetée
		fonction qui retourne une liste d'ingredients
		niveau = page d'une recette
	*/
	$html = file_get_html($html);
	$ret = $html->find('script[type="text/javascript"]');
	foreach ($ret as $r) {
		if (substr($r,0,46) == "<script type=\"text/javascript\">var m_dataLayer") {
			$r = preg_replace('/\s+/', '', $r);
			return explode(",",explode("\",\"recipeType\"",explode("\"contentInfo\":{\"recipeIngredients\":\"",explode(';',$r)[0])[1])[0]);
		}
	}
}

function write_recipe($file,$page) {

	$recipe = new Recipe($page); # classe Recipe du package Marmitoncrawler
	$recipe = $recipe -> getRecipe();

	if (count($recipe)!= 0 and $recipe["type"] == "Plat principal") {

		echo $page."\n";

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
		$a = write_ingredients($page);
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
	}
}

# ============
# === MAIN ===
# ============

$file = fopen('recipes_index_B.txt','a');
fetch_all($file,"http://www.marmiton.org/recettes/recettes-index.aspx");
fclose($file);

?>
