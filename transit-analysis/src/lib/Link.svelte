<script>
	export let link;
  console.log(link)
</script>

<style>
a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}	
/* changes the colour of the drop down item when you hover over them*/
a:hover {background-color: yellow}
</style>


<a href="#{link.toLowerCase()}">{link}</a>
