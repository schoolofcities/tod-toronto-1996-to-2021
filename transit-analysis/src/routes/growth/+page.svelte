<script>

    import TopSofC from "../../lib/TopSofC.svelte";
    import MonthlyChart from "../../lib/MonthlyChart.svelte";
    import Bicycle from "../../assets/bicycle.svg";
    
    import "../../assets/global-styles.css";

    let yTicksTrip = [0, 100000, 200000, 300000, 400000, 500000, 600000, 700000];
    let yTicksStation = [0, 100, 200, 300, 400, 500, 600, 700];
    let yTicksAvStation = [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600];
    let yTicksBike = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000];
    let yTicksAvBikeUsage = [0, 20, 40, 60, 80, 100, 120];

</script>



<TopSofC />

<div class="topImg">
    
        <img
            src="/bike-share-toronto/top-map.png"
            alt="map of bike lanes and bike-share stations in toronto with a green background"
        />
    
</div>

<main>
    

    <MonthlyChart
        variable="AverageBikeUsage"
        yTicks={yTicksAvBikeUsage}
        colour="#8DBF2E"
        maxHeight="300"
        type="line"
    />


</main>


<style>
    /* page specific styling */
    .bike-img {
        max-width: 25px;
        max-height: 15px;
        padding-right: 0px;
    }
</style>
