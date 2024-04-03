<script>
	import TopSofC from "../lib/TopSofC.svelte";
	import LineChart from "../lib/line-chart.svelte";
	import "../assets/global-styles.css";
	import sofcLongCity from "../assets/sofc-long-city.svg";

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
	const lineColour = {
		"Line 1: Yonge-University Subway": "#F1C500",
		"Yonge North Subway Extension": "#F1C500",
		"Line 2: Bloor-Danforth Subway": "#16A753",
		"Scarborough Subway Extension": "#16A753",
		"Line 3: Scarborough RT": "#1F99D5",
		"Line 4: Sheppard Subway": "#B32078",
		"Eglinton Crosstown LRT": "#F87005",
		"Eglinton Crosstown West Extension": "#F87005",
		"Eglinton East LRT": "#F87005",
		"Eglinton Crosstown West Extension - Airport Segment": "#F87005",
		"Finch West LRT": "#888888",
		"Ontario Line": "#1F99D5",
	};

	const textName = {
		"Population":  "the population",
		"Weighted Average Total Individual Income": "the weighted average total individual income",
		"Weighted Average Total Household Income": "the weighted average total household income",
		"Total Occupied Dwellings": "the total count of occupied dwellings",
		"Single-detached house": "the number of households that live in single-detached houses",
		"Semi-detached house": "the number of households that live in semi-detached houses",
		"Row house": "the number of households that live in row houses",
		"Apartment or flat in a -plex*": "the number of households that live in a du-, tri-, four-, multi-plex",
		"Apartment fewer than five storeys": "the number of households that live in apartments/condos that are less than five storeys",
		"Apartment five or more storeys": "the number of households that live in apartments/condos that are in buildings of five or more storeys",
	}

	let topWidth = 200;
</script>

<TopSofC />

<main>
	<div class="title" bind:clientWidth={topWidth}>
		<img width="100%" height="71" src={sofcLongCity} alt="sofcLongCity" />

		<svg width="100%" height="20">
			<line
				x1="2"
				y1="10"
				x2={topWidth - 30 - 5}
				y2="10"
				stroke={lineColour[transitName]}
				stroke-width="5"
				stroke-linecap="round"
			/>
			{#each [0, 1, 2, 3] as c}
				<circle
					r={6}
					cx={8 + c * ((topWidth - 30 - 16) / 3)}
					cy={10}
					stroke-width="4px"
					stroke={lineColour[transitName]}
					fill="#fff"
				/>
			{/each}
		</svg>

		<h1>
			25 Years of Transit-Oriented Development in Toronto: What Has
			Changed?
		</h1>

		<p>
			<a href="https://www.linkedin.com/in/chun-fu-liu/" target="_blank">Michael Liu</a> and <a href="http://jamaps.github.io/" target="_blank">Jeff Allen</a> | April 2024
		</p>
	</div>

	<div class="text">
		<p>
			Toronto has had mixed success in building new housing units where there is easy access to transit service, especially
			along existing and planned subway and light-rail lines.
		</p>
		<p>
			We've created an interactive chart for exploring <a href="https://en.wikipedia.org/wiki/Transit-oriented_development" target="_blank">Transit-Oriented
			Development</a> (TOD), or lack there-of, along Toronto's existing and
			planned major transit lines, specifically for areas within 800
			metres (approximately a 10 minute walk) from these lines. 
		</p>
		<p>	
			Select between lines and different housing data to examine TOD in Toronto. 
			The chart has two curves, one for 1996 and one for 2021, to compare 
			and show changes over this 25 year period.
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
			&nbsp;&nbsp;&nbsp;&nbsp;
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

		<p>

			The chart is currently showing {textName[variableName]} within an
			800m distance of
			{transitName}

			<br><br>

			
			<svg class="legend" height="30px" width={180}>
				<line class="dashed-lines" x1="2px" y1="15" x2="60px" y2="15"
				></line>
				<text x="70px" y="20" font-size="14" fill="white"
					>1996 Census</text
				>
			</svg>
			<svg class="legend" height="30px" width={180}>
				<line class="lines" x1="0px" y1="15" x2="60px" y2="15"></line>
				<text x="70px" y="20" font-size="14" fill="white"
					>2021 Census</text
				></svg
			>
			<!-- key is a function that would destroy the element and rebuilt it upon variable change-->
			
			<br>

			
			<br>
		</p>
		
	</div>
	</main>

	{#key [transitName, variableName]}
		<LineChart
			variable96={variableName + " 96"}
			variable21={variableName + " 21"}
			{transitName}
			colour96="#6FC7EA"
			colour21="#DC4633"
		/>
	{/key}

	<main>
	<div class="text">
		
		<h2>Benefits of TOD</h2>
		<p>
			Transit-oriented developments (TOD) aim for higher density, pedestrian friendly, neighbourhoods near major transit stations. At a local scale, TODs allow people to reduce their reliance on cars for many day-to-day errands and trips. For instance, a resident can safely walk to a nearby stores to get groceries, bike to school, and access the park nearby, all without having the need to rely on cars. For longer trips, living or working to major transit reduces need to travel to work and other further away destinations by car. Overall, reducing car reliance means more physical activity lead to better health outcomes, as well as less carbon emissions and pollution.
		</p>
		<p>
			TOD is also beneficial to city governments, as TOD would locate a large number of residents and jobs, which would encourage people to use public transit and justify the cost of operating and improving these systems. By building more densely, cities can also cut operation and maintenance costs of their infrastructures, such as roads, sewage, water, and waste collection.
		</p>
		<p>
			The charts above show that while a few stations have seen ample development during this 25-year period (e.g. downtown, midtown), most neighbourhoods have seen very little change, and in a few cases, population decline. As Toronto continues to grow and experience population growth, it is imperitive to locate new housing near major transit lines, both existing and those planned to be completed over the coming years. 
		</p>
		<h2>How we created these charts</h2>
		<p>
			Demographic and housing data comes from <a
				href="https://www12.statcan.gc.ca/census-recensement/index-eng.cfm" target="_blank"
				>Statistics Canada’s
			</a>
			Census for 1996 and 2021, respectively. Specifically, we used census data aggregated at the Dissemination Area level data for 2021 and Enumeration Area level data for 1996. These are the smallest geographic areas in which census data is available publicly for each year, respectively. These areas typically consist of a few city blocks. 
		</p>
		<p>
			Transit data on existing and future transit line and transit stations
			were downloaded from <a
				href="https://www.metrolinx.com/en/about-us/open-data" target="_blank"
			>
				Metrolinx's Open Data Catalogue</a
			>. We then used areal interpolation to spatially join this census data to 800 metre buffers, at 400 metre intervals, along each transit line. 800 metres approximately corresponds to a 10 minute walk. We also used Thiessen
			Polygons to determine the closest station for each of the point we generated for display on the charts.
		</p>
		<p>
			The chart was built using <a href="https://d3js.org/" target="_blank">D3</a> and <a href="https://svelte.dev/" target="_blank">Svelte</a>. All our code and data are on <a href="https://github.com/schoolofcities/tod-toronto-1996-to-2021" target="_blank">GitHub</a>.
		</p>
		

		<br>
		<br>
		<br>
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
		margin-top: 8px;
		margin-bottom: 8px;
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
	.legend {
		position: relative;
		/* max-width: 300px; */
		/* top: 0px; */
		margin: 0 auto;
	}
	.dashed-lines {
		position: relative;
		stroke: white;
		margin: 0 auto;
		stroke-dasharray: 2 6;
		stroke-linecap: round;
		margin-bottom: 10px;
		padding-bottom: 20px;
		stroke-width: 4px;
	}
	.lines {
		position: relative;
		margin: 0 auto;
		stroke: white;
		margin-bottom: 10px;
		padding-bottom: 20px;
		stroke-width: 4px;
	}
</style>
