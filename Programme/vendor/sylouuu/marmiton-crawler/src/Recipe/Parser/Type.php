<?php
    namespace sylouuu\MarmitonCrawler\Recipe\Parser;

    use PHPHtmlParser\Dom;

    /**
     * RecipeName Parser
     *
     * @author sylouuu
     * @link https://github.com/sylouuu/marmiton-crawler
     * @version 0.1.0
     * @license MIT
     */
    class Type
    {
        /**
         * Extract from DOM object
         *
         * @param object $dom
         * @return string
         */
        public static function parse ($dom)
        {
            $element = $dom->find('div[class="m_bloc m_content_recette"] div[class="m_bloc_cadre"] div[class="m_content_recette_breadcrumb"]');

            if ($element->text !== null) {
                return utf8_encode(explode(" - ",trim($element->text))[0]);
            } else {
                return null;
            }
        }
    }
