<script>
  import { scaleLinear } from "d3-scale"; // for scaling data to graph the data points
  import jsondata from "../data/data.json"; // import data
  import { line, curveNatural} from "d3";
  import "../assets/global-styles.css";
  import cityAverage from "../data/cityAverage.json";

  export let variable96; //get the selected variable name for 2021
  export let variable21; //get the selected variable name for 2021
  export let colour96; // set colour for 1996
  export let colour21; // set colour for 2021
  export let transitName;

  console.log(transitName);

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

  // Define the mappings between variable96 values and xTick arrays
  const xTickMappings = {
    "Apartment fewer than five storeys 96": [0, 1500, 3000, 4500, 6000],
    "Apartment five or more storeys 96": [0, 12500, 25000, 37500, 50000],
    "Apartment or flat in a -plex* 96": [0, 200, 400, 600, 800, 1000],
    "Movable dwelling 96": [0, 750, 1500, 2250, 3000],
    "Other single-attached house 96": [0, 100, 200, 300, 400],
    "Owner 96": [0, 7500, 15000, 22500, 30000],
    "Owner Renter Ratio 96": [0, 8.75, 17.5, 26.25, 35], // Updated value
    "Population 96": [0, 25000, 50000, 75000, 100000],
    "Renter 96": [0, 8750, 17500, 26250, 35000],
    "Row house 96": [0, 875, 1750, 2625, 3500],
    "Semi-detached house 96": [0, 1375, 2750, 4125, 5500],
    "Single-detached house 96": [0, 1250, 2500, 3750, 5000],
    "Total Occupied Dwellings 96": [0, 13750, 27500, 41250, 55000],
    "Weighted Average number of rooms per dwelling 96": [0, 2.5, 5, 7.5, 10],
    "Weighted Average Total Household Income 96": [
      0, 125000, 250000, 375000, 500000,
    ],
    "Weighted Average Total Individual Income 96": [
      0, 62500, 125000, 187500, 250000,
    ],
  };
  // Set xTick based on variable96 value
  var xTicks = xTickMappings[variable96];

  /* ======= SETTING UP DATA ==========*/

  //filtre data.json to the selected transitName in page.svelte
  function filterDesignation(jsondata) {
    return jsondata["Transit Line"] === transitName;
  }
  // store filtered jsondata in variable called data
  var data = jsondata.filter(filterDesignation);

  /* ======= SETTING UP CHARTING AREAS ==========*/
  const padding = { top: 20, right: 25, bottom: 10, left: 150 };
  let width = 600; // set the base width
  let height = data.length * 5 + padding.top + padding.bottom; // set the base width

  // adjust the width of the graph based on viewing size
  $: innerWidth = (width - (padding.left + padding.right));
  $: innerHeight = height - (padding.top + padding.bottom);

  /* ======= SETTING UP X AND Y AXIS ========== */

  // ------ SETTING UP Y AXIS ------------------------
  // create yTicks
  const yTicks = data.map(function (obj) {
    return obj["Point ID"];
  });

  // ------ SETTING UP X AXIS ------------------------
  // round the numbers for creating xTicks,
  // create xticks using the newMax values
  var xTicks = xTickMappings[variable96];

  // converts thousands and million to K and M i.e. (1,000 ==> 1K , 1,000,000 ==> 1M)
  function thousandToK(tick) {
    var newtick;
    if (tick < 400) {
      newtick = tick;
    } else if (tick >= 1000 && tick < 1000000) {
      newtick = tick / 1000 + "K";
    } else if (tick > 1000000) {
      newtick = tick / 1000000 + "M";
    } else {
      newtick = tick;
    }
    return newtick;
  }

  // ------SETTING UP BARS FOR THE BAR CHART ------------------------
  var barPadding = 1.5; // controls how much spacing the bars will be from the
  // control barwidth based on viewing window width
  $: barWidth = Math.max(Math.min(innerHeight / yTicks.length, 25), 6);

  /* ======= SCALING DATA POINTS ========== */
  $: xScale = scaleLinear()
    .domain([0, Math.max.apply(null, xTicks)])
    .range([padding.left, innerWidth + padding.left - padding.right]);

  $: yScale = scaleLinear()
    .domain([0, yTicks.length])
    .range([padding.top + 10, height - padding.bottom - 2 * barWidth]); // added 0.2*height to accomodate station text label.

  /* ==== SCALING THE LINES === */
  $: line_gen96 = line()
    .curve(curveNatural)
    .x((d) => xScale(d[variable96]))
    .y((d, i) => yScale(i) + barPadding + padding.top)(data);

  $: line_gen21 = line()
    .curve(curveNatural)
    .x((d) => xScale(d[variable21]))
    .y((d, i) => yScale(i) + barPadding + padding.top)(data);



  /* ======= SET UP DATA LABELLING ========== */
  let selected_datapoint = undefined;
  let selected_datapoint_i = undefined;

  // NOT SURE WHAT THIS IS FOR, REMOVE IF UNNECESSARY
  var varName = variable96.replace(" 96", "").replace("Weighted ", "");

  /* MOUSEOVER EVENT */
  let mouse_x, mouse_y;

  const setMousePosition = function (event) {
    mouse_x = event.clientX;
    mouse_y = event.clientY;
  };

  var axis =  padding.left / 2.5
</script>

<div
  id="barchart"
  class="chart"
  bind:clientHeight={height}
  bind:clientWidth={width}
>
  <svg
    height={(data.length + 2) * (barWidth + barPadding) +
      padding.top +
      padding.bottom}
    {width}
  >
    <!-- TEXT LABEL FOR THE STATION NAMES-->
    <g>
      {#each data as point, i}
        {#if point.Label === "Label"}
          <g class="station-tick">
            <text
              x={padding.left - 22}
              y={yScale(i) + barPadding + padding.top + 5}
              text-anchor="end"
							font-size="14"
            >
              {point["Station Name"]}
            </text>
          </g>
        {/if}
      {/each}
    </g>
    <path d={line_gen96} stroke={"white"} stroke-dasharray="6 3"/>
    <path d={line_gen21} stroke={"white"} />
    <!-- CREATE THE LINES ON THE LINE GRAPH-->

    {#each data as point, i}
      <!-- CREATE THE DOTS ON THE LINE GRAPH-->
      <!-- {#if point[variable96] !== null}
        <circle
          class="point"
          r={2}
          cx={xScale(point[variable96])}
          cy={yScale(i) + barPadding + padding.top}
          fill={colour96}
        />
        <circle
          class="point"
          r={2}
          cx={xScale(point[variable21])}
          cy={yScale(i) + barPadding + padding.top}
          fill={colour21}
        />
      {/if} -->
    {/each}

    <!-- CITY AVERAGE VALUES-->
    <!-- <g>
      <line class = "city-average"
        x1={xScale(cityAverage[1][varName])}
        y1={padding.top + 5}
        x2={xScale(cityAverage[1][varName])}
        y2={height - padding.bottom - 1.5 * barWidth}
        stroke={"grey"}
        stroke-width="1"
      />
      <text class = "city-average-text"
        x={xScale(cityAverage[1][varName])+10}
        y={padding.top + 50}
      >2021 City Average: {cityAverage[1][varName]}</text>
    </g> -->


    <!-- X AND Y AXIS-->
    <!-- x axis -->
    <line
      x1={padding.left}
      y1={padding.top + 4}
      x2={padding.left + innerWidth}
      y2={padding.top + 4}
      stroke-width={1}
      stroke={"#fff"}
    />
    {#if innerWidth > 300}
    {#each xTicks as tick, i}
      <text class="text" x={xScale(tick)} y={padding.top} text-anchor="middle"
        >{thousandToK(tick)}
      </text>
			<line
				x1={xScale(tick)}
				y1={padding.top + 4}
				x2={xScale(tick)}
				y2={padding.top + 12}
				stroke-width={1}
				stroke={"#fff"}
			/>
      <line
				x1={xScale(tick)}
				y1={padding.top + 30}
				x2={xScale(tick)}
				y2={height - padding.bottom - 2 * barWidth}
				stroke-width={1}
				stroke={"#4d4d4d"}
			/>
    {/each}
    {/if}
    <!-- y axis -->
    <line
      class="axis y-axis"
      x1={padding.left - 12}
      y1={padding.top + 30}
      x2={padding.left - 12}
      y2={height - padding.bottom - 2 * barWidth}
      stroke-width={6}
      stroke={lineColour[transitName]}
      z-index="3"
    />

    <!-- CREATE STATION TICKS AND LABELS-->

    
    {#each data as point, i}
      <!-- CREATE THE BARS ON THE LINE GRAPH-->
      <!-- <rect
        class="barLight"
				fill={"white"}
        x={padding.left}
        y={yScale(i) + barWidth / 2 - 2 * barPadding}
        width={xScale(Math.max(point[variable21])) - padding.left}
        height={barWidth}
        opacity="0.1"
      />
      <rect
        class="barLight"
				
        x={padding.left}
        y={yScale(i) + barWidth / 2 - 2 * barPadding}
        width={xScale(Math.max(point[variable21])) - padding.left}
        height={barWidth}
        opacity="0"
        on:mouseover={(event) => {
          selected_datapoint = point;
          setMousePosition(event);
          document.querySelector(`#var-text-${i}`).style.opacity = 1;
          document.querySelector(`#var-hover-${i}`).style.opacity = 1;
          selected_datapoint_i = i;
        }}
        on:mouseout={() => {
          // Reset the opacity of var-text when the mouse leaves the bar
          document.querySelector(`#var-text-${i}`).style.opacity = 0;
          document.querySelector(`#var-hover-${i}`).style.opacity = 0;
        }}
      /> -->
      <!-- LABELLING THE DATA WILL SHOW ON HOVERING THE BARS-->
      <!-- <rect
        id={`var-hover-${i}`}
        class="var-hover"
        x={padding.left + innerWidth}
        y={yScale(i) + barWidth / 2 - 2 * barPadding}
        width={500}
        height={barPadding + 3 * barWidth}
        opacity="0"
      />
      <text
        id={`var-text-${i}`}
        class="var-text"
        x={padding.left + innerWidth}
        y={yScale(i) + barPadding + padding.top + 5}
        >
        <tspan
          x={[xScale(Math.max(point[variable21])) + 5]}
					dy={-8}
          fill={lineColour[transitName]}
          >{"1996: " + Math.round(point[variable96] * 100) / 100}</tspan
        >
        <tspan
          x={xScale(Math.max(point[variable21])) + 5}
          dy={15}
          fill={lineColour[transitName]}
          >{"2021: " + Math.round(point[variable21] * 100) / 100}</tspan
        >
      </text> -->
    {/each}

		<!-- Line that marks the location of the station-->
    <g class="station-lines">
      {#each data as point, i}
        {#if point.Label === "Label" && i + 1 < data.length}
          <line
            class="station-sep-lines"
            x1={padding.left + innerWidth}
            y1={yScale(i) + barPadding + padding.top}
            x2={padding.left}
            y2={yScale(i) + barPadding + padding.top}
            stroke-width={1}
            stroke="#fff"
            stroke-dasharray="5 3"
            opacity="0.1"
          />
          <circle
            class="point"
            r={6}
            cx={padding.left - 12}
            cy={yScale(i) + barPadding + padding.top}
            stroke-width="4px"
            stroke={lineColour[transitName]}
            fill="#FFFFFF"
          />
        {/if}

        <!--Special label position for the last tick-->
        {#if point.Label === "Label" && i + 1 === data.length}
          <line
            class="station-sep-lines"
            x1={innerWidth - padding.right}
            y1={yScale(i) + barPadding + padding.top}
            x2={padding.left}
            y2={yScale(i) + barPadding + padding.top}
            stroke-width={1}
            stroke="#fff"
            stroke-dasharray="5 3"
            opacity="0.1"
          />
          <circle
            class="point"
            r={6}
            cx={padding.left - 12}
            cy={yScale(i) + barPadding + padding.top}
            stroke-width="4px"
            stroke={lineColour[transitName]}
            fill="#FFFFFF"
          />
        {/if}
      {/each}
    </g>
  </svg>
</div>

<style>
  /* CHART */
  .chart {
    /* width: 80%; */
    /* left: 0%; */
    max-width: 1000px;
		min-width: 500px;
  }

  svg {
    position: relative;
    /* width: 90%; */
    /* left: 5%; */
    z-index: 2;
  }

  .city-average {
    stroke-width: 5px;
    z-index: 1;
    stroke: white;
    opacity: 0.5;
  }
  .city-average-text {
    font-size: 15px;
    font-weight: bold;
    fill: #ffffff;
  }

  /* XY axis */
  .text {
    fill: white;
    font-size: 16px;
    background-color: lightgrey;
    font-weight: bold;
  }

  /* AXIS */
  .station-lines {
    stroke-width: 5px;
  }

  .station-tick {
    text-anchor: right;
    word-wrap: break-word;
  fill: var(--brandGray);
  font-size: 17px;
  text-align: right;
  max-width: 15px; /* Adjust the value as needed */
  /* Optional: Enable text wrapping */
  white-space: pre-line; /* Allow line breaks */
  }
  .station-box{
    width: 200px;
    height: 300px;
    background-color: red;
  }

  /* LINES GRAPH */
  .point {
    cursor: pointer;
  }
  .point:hover {
    fill: var(--brandLightBlue);
    opacity: 1;
  }

  /* BAR GRAPH */
  .barLight {
    z-index: -5;
  }

  .barLight:hover {
    opacity: 0;
    cursor: pointer;
    z-index: 1;
  }

  /* HOVERING */
  #hoverLabel {
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .var-text {
    opacity: 0;
    padding-top: 5px;
    padding-left: 14px;
    font-size: 12px;
    font-weight: bold;
  }
  .var-hover {
    fill: black;
  }
  path {
    fill: transparent;
    stroke-width: 4;
    stroke-linejoin: round;
		z-index: 40;
  }
</style>
