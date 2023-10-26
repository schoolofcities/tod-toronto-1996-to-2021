<script>
    import TopSofC from "../lib/TopSofC.svelte";
    import LineChart from "../lib/line-chart.svelte";
    import "../assets/global-styles.css";
    import Map from "../lib/map.svelte";
    //import Link from "../lib/Link.svelte";
    //import Button from "../lib/Button.svelte";
    //import DropDown from "../lib/SelectVariable.svelte"

    let transitName = "Bloor-Danforth Subway";
    var variableName = "Adjusted Weighted Income";

    var variable_1996 = variableName + " 1996";
    var variable_2021 = variableName + " 2021";

    console.log(variable_1996);
    console.log(variable_2021);

    var censusItems = [
        "Population",
        "Total Occupied Dwelling",
        "Single-detached",
        "Semi-detached",
        "Row House",
        "Apartment or Duplex",
        "Apartment fewer than 5 STY",
        "Apartment greater than 5 STY",
        "Adjusted Weighted Income",
    ];

    // Section on Drop Down List
    let initialTransitVariable;
    let initialCensusVariable;
    var transit_lines = [
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
    function handleTransitChange(event) {
        const selectedValue = event.target.value;
        //console.log(selectedValue);
        transitName = selectedValue;
        //selectedVariable.set(selectedValue);
    }
    function handleCensusChange(event) {
        const selectedValue = event.target.value;
        //console.log(selectedValue);
        variableName = selectedValue;
        //selectedVariable.set(selectedValue);
    }
</script>

<TopSofC />
<h1>
    25 Years of Transit-Oriented Development, What Has Changed?
</h1>

<p>
    Here we insert some text about the transit-oriented policy. 
</p>





<select id = "transit" value={transitName} on:change={handleTransitChange}>
    {#each transit_lines as value}
        <option {value}>{value}</option>
    {/each}
</select>
<select id = "census" value={variableName} on:change={handleCensusChange}>
    {#each censusItems as value}
        <option {value}>{value}</option>
    {/each}
</select>



<!-- key is a function that would destroy the element and rebuilt it upon variable change-->
{#key [transitName, variableName]}
<LineChart 
    variable96={variableName + " 1996"}
    variable21={variableName + " 2021"}
    transitName = {transitName}
    colour="#6FC7EA"
    colour2="#8DBF2E"
    maxHeight="700"
/>
<Map/>
{/key}




<h3>
    Methodology
</h3>
<p>
    The data for this graph is collected in Statistics Canada's Census for the year of 1996
    and 2021. 
    <br>
    Created points every 400m along each transit line. <br>
    Created 800 metres buffer for each of the points created. <br>
    Spatial interpolation and weighted average to estimate the amount of each variable that is within the 800m buffers. 
    
</p>


<style>
    h1{
        margin-left: 10%;
        margin-top: 5%;
    }
    h3{
        margin-left: 10%;
        margin-top: 5%;
    }
    select {
        padding-left: 0%;
        max-width: 600px;
        max-width: calc(100vw - 30px);
        background-color: var(--brandGray90);
        border: 1px solid var(--brandDarkBlue);
        color: white;
        font-size: 22px;
    }
    #transit{
        margin-left: 10%;
        margin-bottom: 1%;
    }
    #census{
        margin-left: 0%;
    }
    select option {
        padding-left: 10%;
        background-color: var(--brandGray90);
        color: white;
    }

    select:hover {
        
        cursor: pointer;
        background-color: var(--brandDarkBlue);
    }
    p {
        padding-left: 10%;;
    }


    @media only screen and (max-width: 500px) {
    h1{
        margin-left: 5%;
        margin-right: 0%;
    }
    h3{
        margin-left: 5%;
    }
    #transit{
        margin-left: 5%;
    }
    #census{
        margin-left: 5%;
    }
    p {
        padding-left: 5%;;
    }
}
</style>
