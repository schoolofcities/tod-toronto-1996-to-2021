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
		"Weighted Average Total Individual Income": "weighted average total individual income",
		"Weighted Average Total Household Income": "weighted average total household income",
		"Total Occupied Dwellings": "total count of occupied dwellings",
		"Single-detached house": "count of people who live in single-detached house",
		"Semi-detached house": "count of people who live in semi-detached house",
		"Row house": "count of people who live in row house ",
		"Apartment or flat in a -plex*": "number of apartments or flats in a du-, tri-, four-, multi-plex",
		"Apartment fewer than five storeys": "number of apartments that are less than five storeys",
		"Apartment five or more storeys": "number of apartments that are in buildings five or more storeys",
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
			<a href="">Michael Liu</a> and <a href="">Jeff Allen</a>
		</p>
	</div>

	<div class="text">
		<p>
			Toronto has had mixed success in building new housing
			units where there is easy access to transit services, especially
			along subway and light-rail lines.
		</p>
		<p>
			We've created an interactive chart for exploring Transit-Oriented
			Development (TOD), or lack there-of, along Toronto's existing and
			planned major transit lines, specifically for areas within 800
			metres (approx. a 10-15 minute walk) from these lines. 
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

		<p>
			The chart is currently showing <b>{textName[variableName]}</b> in the area that is within
			<b>800m</b> distance of 
			<b>{transitName}</b><br />

			<svg class="legend" height="30px" width={600}>
				<line class="dashed-lines" x1="0px" y1="15" x2="60px" y2="15"
				></line>
				<text x="70px" y="20" font-size="14" fill="white"
					>1996 Census</text
				>
			</svg>
		</p>
		<p>
			<svg class="legend" height="30px" width={600}>
				<line class="lines" x1="0px" y1="15" x2="60px" y2="15"></line>
				<text x="70px" y="20" font-size="14" fill="white"
					>2021 Census</text
				></svg
			>
			<!-- key is a function that would destroy the element and rebuilt it upon variable change-->
		</p>
		{#key [transitName, variableName]}
			<LineChart
				variable96={variableName + " 96"}
				variable21={variableName + " 21"}
				{transitName}
				colour96="#6FC7EA"
				colour21="#DC4633"
			/>
		{/key}
	</div>

	<div class="text">
		<h2>What Is Transit Oriented Development?</h2>
		<p>
			Transit-oriented development (TOD) is a way of building the cities
			transit-infrastructures. A TOD project is usually higher density,
			meaning around transit-infrastructures. A TOD project is usually
			higher that it is a more efficient use of land to house people, jobs
			and other density, meaning that it is a more efficient use of land
			to house activities. When TOD is applied to a community level, the
			area would be people, jobs and other activities. When TOD is applied
			to a built to be pedestrian friendly so its residents can have easy
			access to community level, the area would be built to be pedestrian
			friendly public transit. The area would also be amenity rich,
			providing a range of so its residents can have easy access to public
			transit. The area services and job opportunities. Through TOD, a
			community will become a place would also be amenity rich, providing
			a range of services and job where people can live, work, and play.
			opportunities. Through TOD, a community will become a place where
			people can live, work, and play.

			<br />
			<br /><b>What is the benefit of TOD? </b><br />

			TOD allows people to reduce their reliance on cars for many errands.
			For instance, a resident can simply walk to a nearby grocery store
			to get groceries, bike a few blocks to get to the place where they
			are employed, and access the park nearby, all without having the
			need to rely on cars. Through reducing reliance on cars, people will
			not have to allocate a portion of their income to buy and operate a
			car. TOD encourages people to walk and bike more, which can in turn
			help people exercise, reducing the level of obesity and the diseases
			caused by it. It is also beneficial to our environment as we reduce
			the amount of carbon emissions and harmful air pollution particles
			that would cause respiratory issues.
			<br /> <br />
			TOD is also beneficial to city governments, as TOD would locate a large
			number of residents and jobs, which would encourage people to use public
			transit and justify the cost of operating these systems. By building
			more densely, cities can also cut operation and maintenance costs of
			their infrastructures, such as roads, sewage, water, and waste collection.
		</p>

		<h2>How we created these charts</h2>
		<p>
			Transit-Oriented Developments are often defined as areas within 5-to-15
			minute walk to major transit service (e.g. metro, commuter rail, BRT/LRT). 
			The chart above specifically compares data from <a
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
	.legend {
		position: relative;
		max-width: 300px;
		top: 10px;
		margin: 0 auto;
	}

	.dashed-lines {
		position: relative;
		stroke: white;
		margin: 0 auto;
		stroke-dasharray: 6 3;
		margin-bottom: 10px;
		padding-bottom: 20px;
		stroke-width: 5px;
	}
	.lines {
		position: relative;
		margin: 0 auto;
		stroke: white;
		margin-bottom: 10px;
		padding-bottom: 20px;
		stroke-width: 5px;
	}
</style>
