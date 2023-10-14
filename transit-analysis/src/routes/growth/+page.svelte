<script>

    import TopSofC from "../../lib/TopSofC.svelte";
    import LineChart from "../../lib/line-chart.svelte";
    import "../../assets/global-styles.css";

    let yTicksTrip = [25000, 40000, 50000,60000,70000,80000,90000,100000,110000,120000,130000,140000];
    let yTicksStation = [0, 100, 200, 300, 400, 500, 600, 700];
    let yTicksAvStation = [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600];
    let yTicksBike = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000];
    let yTicksAvBikeUsage = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 2500];

    var transitName = "Ontario Line"  
    var variableName = "Adjusted Weighted Income"

    variableName = variableName.replaceAll(" ", "_")

    var variable_1996 = variableName + "_1996"
    var variable_2021 = variableName + "_2021"

</script>



<TopSofC />


<main>
    <p>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
    </p>
    
    <LineChart
        variable= {variable_1996}
        variable2 = {variable_2021}
        transitName = {transitName}
        yTicks={yTicksTrip}
        colour="#6FC7EA"
        colour2 = "#8DBF2E"
        maxHeight="500"
        
    />



</main>


<style>
 
</style>
