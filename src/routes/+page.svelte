<script>
    import TopSofC from "../lib/TopSofC.svelte";
    import LineChart from "../lib/line-chart.svelte";
    import "../assets/global-styles.css";

    let transitName = "Line 2: Bloor-Danforth Subway";
    var variableName = "Population";

    var censusItems = [
        "Population",
        "Weighted Average Total Individual Income",
        "Weighted Average Total Household Income",
        "Total Occupied Dwellings",
        "Single-detached house",
        "Semi-detached house",
        "Row house",
        "Apartment or flat in a -plex*",
        "Apartment fewer than five storeys",
        "Apartment five or more storeys",
        // "Weighted Average number of rooms per dwelling",
        // "Owner",
        // "Renter",
        // "Owner Renter Ratio",
    ];

    var transit_lines = [
        "Line 1: Yonge-University Subway",
        "Yonge North Subway Extension",
        "Line 2: Bloor-Danforth Subway",
        "Scarborough Subway Extension",
        "Line 3: Scarborough RT",
        "Line 4: Sheppard Subway",
        "Eglinton Crosstown LRT",
        "Eglinton Crosstown West Extension",
        // "Eglinton Crosstown West Extension - Airport Segment",
        "Eglinton East LRT",
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

<main>
    <div class="title">
        <h1>
            25 Years of Transit-Oriented Development:<br />What Has Changed?
        </h1>

        <p>
            <a href="">Michael Liu</a> and <a href="">Jeff Allen</a>
        </p>
    </div>

    <div class="text">
        <p>
            Toronto has been encouraging building new housing units along places
            where there is easy access to transit services, especially along
            subway and light-rail services, usually in areas within 500 to 800
            metres. This urban development approach is also known as
            Transit-Oriented Developments (TOD).
        </p>
        <p>
            This widget is designed to show changes along Toronto Transit
            Commission (TTC)'s Light Rail and Subway lines, for areas within 800
            metres (15-minute walk). You can view the changes for existing and
            planned transit services. In addition, we have also picked a few
            interesting aspects of TOD that we would like to explore, these
            aspects include population, income and dwelling types.
        </p>
        <p>
            The chart is currently showing the <b>{variableName}</b> that is
            within an <b>800m</b> distance from each point on the
            <b>{transitName}</b>
        </p>

        <p>
            <select
                id="transit"
                value={transitName}
                on:change={handleTransitChange}
            >
                {#each transit_lines as value}
                    <option {value}>{value}</option>
                {/each}
            </select>
        </p>
        <p>
            <select
                id="census"
                value={variableName}
                on:change={handleCensusChange}
            >
                {#each censusItems as value}
                    <option {value}>{value}</option>
                {/each}
            </select>
        </p>
    </div>

    <!-- key is a function that would destroy the element and rebuilt it upon variable change-->
    {#key [transitName, variableName]}
        <div class="chart">
            <LineChart
                variable96={variableName + " 96"}
                variable21={variableName + " 21"}
                {transitName}
                colour96="#6FC7EA"
                colour21="#DC4633"
            />
        </div>
    {/key}

    <div class="text">
        <h2>What Is Transit Oriented Development?</h2>
        <p>
            Transit-oriented development (TOD) is a way of building the cities
            around transit-infrastructures. A TOD project is usually higher
            density, meaning that it is a more efficient use of land to house
            people, jobs and other activities. When TOD is applied to a
            community level, the area would be built to be pedestrian friendly
            so its residents can have easy access to public transit. The area
            would also be amenity rich, providing a range of services and job
            opportunities. Through TOD, a community will become a place where
            people can live, work, and play.
            <br />
            <br /><b>What is the benefit of TOD? </b><br />
            TOD allows people to reduce their reliance on cars for many errands.
            For instance, a resident can simply walk to a nearby grocery store to
            get groceries, bike a few blocks to get to the place where they are employed,
            and access the park nearby, all without having the need to rely on cars.
            Through reducing reliance on cars, people will not have to allocate a
            portion of their income to buy and operate a car. TOD encourages people
            to walk and bike more, which can in turn help people exercise, reducing
            the level of obesity and the diseases caused by it. It is also beneficial
            to our environment as we reduce the amount of carbon emissions and harmful
            air pollution particles that would cause respiratory issues.
            <br /> <br />
            TOD is also beneficial to city governments, as TOD would locate a large
            number of residents and jobs, which would encourage people to use public
            transit and justify the cost of operating these systems. By building
            more densely, cities can also cut operation and maintenance
            costs of their infrastructures, such as roads, sewage, water, and waste
            collection.
        </p>

        <h2>Methodology</h2>
        <p>
            Transit-Oriented Developments are defined as areas within 5-10
            minutes walk to a transit service. In Ontario, this is equivalent to
            500 to 800 metres. This widget compares data from <a
                href="https://www12.statcan.gc.ca/census-recensement/index-eng.cfm"
                >Statistics Canada’s
            </a>
            Census for the year of 1996 and 2021. Census data agglomerates data to
            multiple geographical areas, from city level data to the smallest and
            publicly available level, Dissemination Area level data, which is consisted
            of a few city blocks. This widget uses Dissemination Area to get the
            most accurate estimate of the census variables. Due to the boundary of
            800-metre buffers do not align with Dissemination Area boundaries, we
            used areal interpolation to estimate the density of each variable within
            respective Dissemination Areas, then interpolate the data by the area
            that is within the 800 metre buffer. <br />
        </p>
        <p>
            We generated points every 400 meters along transit-services in
            Toronto, then created 800-meter buffers around the generated points.
            Since transit stations are not 400m apart, We also used Thiessen
            Polygon to determine the closest station for each of the point we
            generated.
            <br />
        </p>
        <p>
            All transit layers, including the transit line and transit stations,
            were downloaded from <a
                href="https://www.metrolinx.com/en/about-us/open-data"
            >
                Metrolinx's Open Data Catalogue</a
            >
        </p>
    </div>
</main>

<style>
    select {
        padding: 3px;
        padding-left: 5px;
        width: 340px;
        background-color: var(--brandBlack);
        border: 1px solid var(--brandBlack);
        color: white;
        font-size: 16px;
        border-color: var(--brandGray70);
        border-radius: 1px;
    }
    select option {
        background-color: var(--brandGray90);
        color: white;
        stroke: white;
    }

    select:hover {
        cursor: pointer;
        background-color: var(--brandDarkBlue);
    }

    .chart {
        max-width: 1046px;
        background-color: none;
        margin: 0 auto;
        position: relative;
    }
</style>
