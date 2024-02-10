<script>
    //import { data } from "./utils.js";
    import data from "../data/data.json";
    //import Header from "./Header.svelte";
    import LineChart from "../lib/line-chart.svelte";

    console.log(data)
</script>

<style>
  :global(*) {
    box-sizing: border-box;
    padding: 0;
    margin: 0;
  }
  :global(body) {
    font-family: "Cabin", sans-serif;
  }

  :global(#root) {
    width: 90vw;
    max-width: 550px;
    margin: 0.5rem auto;
    padding: 0 0.5rem;
  }
  :global(#root > * + *) {
    margin-top: 1.5rem;
  }
</style>

<svelte:head>

</svelte:head>

<div id="root">
    <!-- each line chart component receives through props an array of objects detailing the values and dates -->
    <LineChart title="106th Edition - Population" dataset="{data}"/>
</div>

