<script>
    import TopSofC from "../lib/TopSofC.svelte";
    import LineChart from "../lib/line-chart.svelte";
    import "../assets/global-styles.css";
    import Map from "../lib/map.svelte";

    let transitName = "Line 2: Bloor-Danforth Subway";
    var variableName = "Weighted Value Average Total Individual Income";

    var censusItems = [
        "Population",
        "Weighted Value Average Total Individual Income",
        "Weighted Value Average Total Household Income",
        "Weighted Value Average number of rooms per dwelling",
        "Total Occupied Dwellings",
        "Single-detached house",
        "Semi-detached house",
        "Apartment or flat",
        "Apartment fewer than five storeys",
        "Apartment five or more storeys",
        "Owner",
        "Renter",
        "Owner Renter Ratio",
    ];

    // Section on Drop Down List
    var transit_lines = [
        "Line 1: Yonge-University Subway",
        "Yonge North Subway Extension",
        "Line 2: Bloor-Danforth Subway",
        "Scarborough Subway Extension",
        "Line 3: Scarborough RT",
        "Line 4: Sheppard Subway",
        "Eglinton Crosstown LRT",
        "Eglinton Crosstown West Extension",
        "Eglinton East LRT",
        "Eglinton Crosstown West Extension - Airport Segment",
        "Finch West LRT",
        "Ontario Line",
    ];
    function handleTransitChange(event) {
        const selectedValue = event.target.value;
        console.log(selectedValue);
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
<h1>25 Years of Transit-Oriented Development, What Has Changed?</h1>

<select id="transit" value={transitName} on:change={handleTransitChange}>
    {#each transit_lines as value}
        <option {value}>{value}</option>
    {/each}
</select>
<select id="census" value={variableName} on:change={handleCensusChange}>
    {#each censusItems as value}
        <option {value}>{value}</option>
    {/each}
</select>

<!-- key is a function that would destroy the element and rebuilt it upon variable change-->
{#key [transitName, variableName]}
    <LineChart
        variable96={variableName + " 96"}
        variable21={variableName + " 21"}
        {transitName}
        colour="#6FC7EA"
        colour2="#8DBF2E"
        maxHeight="700"
    />
{/key}

{#key transitName}
    <Map {transitName} />
{/key}

<h2>A Brief Background On Transit Oriented Development </h2>
<p>
    Transit-Oriented Development (TOD) is a city-building concept that encourages cities to direct their population 
    and economic growth surrounding public transportation systems, especially around subway, LRT, and commuter rail stations. 
    By promoting TOD, residents can enjoy easy access to public transit and a range of amenities that allow them to live, work, 
    and play within proximity to their homes. TOD is expected to help reduce our reliance on cars. In recent years, the Government 
    of Ontario has required municipalities to delineate "Major Transit Station Areas" surrounding their subways, LRTs, BRTs, and GO train 
    stations. These areas are usually within 500 to 800 meters of one of these stations. Municipalities are required to direct and encourage 
    higher-density developments to achieve a minimum population and job density. This web page examines the Subway and LRT system in Toronto, 
    including those that currently exist, are under construction, and are planned. We plot points every 400 meters along each transit line, then 
    calculate the results for various census variables.
</p>

<h2>Methodology</h2>
<p>
    The information presented in the line chart is obtained by processing Census data released by <a href = "https://www12.statcan.gc.ca/census-recensement/index-eng.cfm">
    Statistics Canada</a> for the years 1996 and 2021. To calculate the changes in census variables near 
    Transit Services, we generated points along Toronto's transit lines, including all higher-order 
    public transit services (excluding GO Transit routes). These services include currently existing 
    and planned routes. Planned routes are included because developments can happen in an area before 
    the opening of a transit line (e.g., Eglinton Crosstown, Yonge-North Subway Extension).
    <br>
</p>
<p>
    We generated points every 400 meters along the transit line and then created 800-meter buffers around the generated points. 
    The buffers are used to crop Census Dissemination Area boundaries for 1996 and 2021. When a Dissemination Area is only partially within the buffer, 
    area interpolation is used to estimate the values that fall within the transit buffers. All variables except the weighted variables are the sum of the 
    interpolated values within the transit buffers. The weighted values are based on the area of the Dissemination Area within the transit buffer, compared 
    to the areas of other Dissemination Areas within the same transit buffer.
    <br>
</p>
<p>
    All transit layers, including the transit line and transit stations, were downloaded from <a href = "https://www.metrolinx.com/en/about-us/open-data"
    > Metrolinx's Open Data Catalogue</a>
</p>

<style>
    h1 {
        margin-left: 10%;
        margin-top: 5%;
    }
    h2 {
        margin-left: 5%;
        margin-top: 1%;
    }
    main {
        margin-left: 5%;
        margin-bottom: 5%;
        margin-right: 5%;
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
    #transit {
        margin-left: 10%;
        margin-bottom: 1%;
    }
    #census {
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
        
        padding-left: 5%;
        padding-right: 5%;
        padding-bottom: 2px;
        font-size: 20px;
    }

    @media only screen and (max-width: 1258px) {
        h1 {
            margin-left: 5%;
            margin-right: 0%;
        }
        h2 {
            margin-left: 5%;
        }
        #transit {
            margin-left: 5%;
        }
        #census {
            margin-left: 5%;
        }
        p {
            padding-left: 5%;
        }
        select option {
            padding-left: 20%;
            padding-right: 20%;
            background-color: var(--brandGray90);
            color: white;
        }
    }
    @media only screen and (max-width: 800px) {
        h1 {
            margin-left: 2%;
            margin-right: 0%;
        }
        h2 {
            margin-left: 2%;
        }
        #transit {
            margin-left: 2%;
        }
        #census {
            margin-left: 2%;
        }
        p {
            padding-left: 2%;
        }
        select option {
            padding-left: 2%;
            padding-right: 2%;
            background-color: var(--brandGray90);
            color: white;
        }
    }
</style>
