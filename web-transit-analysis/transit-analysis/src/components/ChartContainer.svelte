<script>
    import LineChart from "./LineChart.svelte";

    export let type ;
    export let chartProps;

    const CHART_TYPES = {
        lineChart : LineChart,
    };


</script>

<section class = "container">
    <svelte:component this = {CHART_TYPES[type]} {...chartProps}/>
</section>

<style>
    .container{
        max-width: 640px;
        border: solid 2px black;
        margin: auto;
    }
</style>