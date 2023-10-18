<script>
    import TopSofC from "../../lib/TopSofC.svelte";
    import LineChart from "../../lib/line-chart.svelte";
    import "../../assets/global-styles.css";
    import Link from "../../lib/Link.svelte";
    import Button from "../../lib/Button.svelte";

    let yTicksTrip = [
        25000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000,
        130000, 140000,
    ];
    let yTicksStation = [0, 100, 200, 300, 400, 500, 600, 700];
    let yTicksAvStation = [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600];
    let yTicksBike = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000];
    let yTicksAvBikeUsage = [
        0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 2500,
    ];

    let transitName = "Ontario Line";
    var variableName = "Adjusted Weighted Income";

    variableName = variableName.replaceAll(" ", "_");

    var variable_1996 = variableName + "_1996";
    var variable_2021 = variableName + "_2021";

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
    function handleItemClick(item) {
        console.log("Clicked on item: " + item);
        // You can perform other actions related to the clicked item here
    }

    let languages = ["sk", "cz", "en", "at"];
    let activeLang = "en";
</script>

<TopSofC />
<p>
    <br />
    <br />
    <br />
</p>
<h1>Active: {console.log(transitName)}</h1>
<ul>
    {#each transitItems as transit}
        <li on:click={(event) => (transitName = event.target.innerText)}>
            {transit}
        </li>
    {/each}
</ul>
<LineChart
    variable={variable_1996}
    variable2={variable_2021}
    {transitName}
    yTicks={yTicksTrip}
    colour="#6FC7EA"
    colour2="#8DBF2E"
    maxHeight="500"
/>
{console.log(transitName)}
<section class="dropdown">
    <Button
        on:click={() => (transitOpen = !transitOpen)}
        {transitOpen}
        buttonName="Transit Lines"
    />

    <div id="myDropdown" class:show={transitOpen} class="dropdown-content">
        <!-- MENU -->
        {#each transitItems as item}
            <Link link={item} on:click={() => handleItemClick(item)} />
        {/each}
    </div>
</section>
<section class="dropdown">
    <Button
        on:click={() => (censusOpen = !censusOpen)}
        {censusOpen}
        buttonName="Census Variables"
    />

    <div id="myDropdown" class:show={censusOpen} class="dropdown-content">
        <!-- MENU -->
        {#each censusItems as item}
            <Link link={item} on:click={() => handleItemClick(item)} />
        {/each}
    </div>
</section>

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
