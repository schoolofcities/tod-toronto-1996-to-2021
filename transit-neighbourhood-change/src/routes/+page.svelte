<script>
    import TopSofC from "../lib/TopSofC.svelte";
    import LineChart from "../lib/line-chart.svelte";
    import "../assets/global-styles.css";
    //import Link from "../lib/Link.svelte";
    //import Button from "../lib/Button.svelte";

    let transitName = "Bloor-Danforth Subway";
    var variableName = "Adjusted Weighted Income";
   

    var variable_1996 = variableName + " 1996";
    var variable_2021 = variableName + " 2021";

    console.log(variable_1996)
    console.log(variable_2021)
    let transitOpen = false;
    let censusOpen = false;
    let inputValue = "";
    $: console.log(inputValue);

    const transitItems = [
        "Yonge-University Subway",
        "Spadina Subway Extension",
        "Yonge North Subway Extension",
        "Bloor-Danforth Subway",
        "Scarborough Subway",
        "Scarborough RT",
        "Sheppard Subway",
        "Sheppard East",
        "Eglinton Crosstown LRT",
        "Finch West LRT",
        "Ontario Line",
    ];
    const censusItems = [
        "Population",
        "Total Occupied Dwelling",
        "Single detached",
        "Semi detached",
        "Row House",
        "Apartment or Duplex",
        "Apartment fewer than 5 STY",
        "Apartment greater than 5 STY",
        "Other Single Detached",
        "Adjusted Weighted Income",
    ];
  
</script>

<TopSofC />
<p>
    <br />
    <br />
    <br />
</p>

<LineChart
    variable96={variable_1996}
    variable21={variable_2021}
    transitName = {transitName}
    colour="#6FC7EA"
    colour2="#8DBF2E"
    maxHeight="700"
/>


<p>
    <br />
</p>

<style>
    .dropdown {
        position: relative;
        display: inline-block;
    }

    .dropdown-content {
        display: none;
        position: absolute;
        background-color: #f6f6f6;
        min-width: 230px;
        border: 1px solid #ddd;
        z-index: 1;
    }

    /* Show the dropdown menu */
    .show {
        display: block;
    }
</style>
