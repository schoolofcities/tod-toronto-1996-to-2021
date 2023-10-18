<script>
	
    export let buttonName;
    
    let show = false;

</script>

<style>	
/* Dropdown Button */
.dropbtn {
  background-color: #DC4633;
  color: white;
  padding: 10px;
  font-size: 20px;
  border: none;
  cursor: pointer;
  font-family: "Arial";
}
	
	/* Dropdown button on hover & focus */
.dropbtn:hover, .dropbtn:focus {
  background-color: #8DBF2E;
  background-color: #DC4633;
  color: white;
  padding: 10px;
  font-size: 20px;
  border: none;
  cursor: pointer;
  font-family: "Arial";
}

</style>
{#if true}
  <button on:click class="dropbtn">{buttonName}</button>
  
{/if}