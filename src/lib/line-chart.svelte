<script>
  import { scaleLinear } from "d3-scale"; // for scaling data to graph the data points
  import jsondata from "../data/data.json"; // import data
  import { onMount, onDestroy } from "svelte";
  import "../assets/global-styles.css";
  import cityAverage from "../data/cityAverage.json";

  //export let data;
  export let variable96; //get the selected variable name for 2021
  export let variable21; //get the selected variable name for 2021
  export let colour96; // set colour for 1996
  export let colour21; // set colour for 2021
  export let transitName;

  /*{selected_datapoint["Station Name"].toString().toLocaleString() + " (" +
          selected_datapoint["Count"] + ")" +" " + "1996" + selected_datapoint[variable96].toLocaleString()+ 
          "2021 "+ selected_datapoint[variable21].toLocaleString()}*/

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
    "Apartment or flat 96": [0, 500, 1000, 1500, 2000],
    "Movable dwelling 96": [0, 750, 1500, 2250, 3000],
    "Other single-attached house 96": [0, 100, 200, 300, 400],
    "Owner 96": [0, 7500, 15000, 22500, 30000],
    "Owner Renter Ratio 96": [0, 8.75, 17.5, 26.25, 35], // Updated value
    "Population 96": [0, 22500, 45000, 67500, 90000],
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
  const padding = { top: 20, right: 60, bottom: 10, left: 35 };
  let width = 600; // set the base width
  let height = data.length * 5 + padding.top + padding.bottom; // set the base width

  // adjust the width of the graph based on viewing size
  $: innerWidth = 0.85*(width - (padding.left + padding.right));
  $: innerHeight = height - (padding.top + padding.bottom);

  $: console.log(innerWidth)
  /* ======= SETTING UP X AND Y AXIS ========== */

  // ------ SETTING UP Y AXIS ------------------------
  // create yTicks
  const yTicks = data.map(function (obj) {
    return obj["Point ID"];
  });

  // ------ SETTING UP X AXIS ------------------------
  // find the max value of the selected 1996 and 2021 variable (furthest to the right of the webpage)
  // this is to identify how long the bars should be, so that it always extend to the higher value between the 1996 value and 2021 value
  // xMax will return a list of the larger values between 1996 and 2021.
  var xMax = data.map(function (obj) {
    var max = Math.max(obj[variable96], obj[variable21]);
    return max;
  });
  // find the largest value of xMax
  var max = Math.max.apply(Math, xMax);

  // round the numbers for creating xTicks,
  // this is because we want the chart to only return rounded numbers. (i.e. 100, 2000, 30000)
  var digits = max.toExponential().split("e+");
  // return the smallest integer greater than the input value
  var roundedValue =
    Math.ceil(parseFloat(digits[0])) * 10 ** parseInt(digits[1]);
  var interval = roundedValue / 10;

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
    var barPadding = 1; // controls how much spacing the bars will be from the
  // control barwidth based on viewing window width
  $: barWidth = Math.max(Math.min(innerHeight / yTicks.length, 25), 6);

  /* ======= SCALING DATA POINTS ========== */
  $: xScale = scaleLinear()
    .domain([0, Math.max.apply(null, xTicks)])
    .range([padding.left, innerWidth - padding.right]);

  $: yScale = scaleLinear()
    .domain([0, yTicks.length])
    .range([padding.top + 10, height - padding.bottom - 2*barWidth]); // added 0.2*height to accomodate station text label.



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

  console.log(varName);
</script>

<div id="barchart" class="chart" bind:clientHeight={height} bind:clientWidth={width} >
  <svg
    height={(data.length+2) * (barWidth + barPadding) +
      padding.top +
      padding.bottom}
      width =  {width}
  >
    <!-- TEXT LABEL FOR THE STATION NAMES-->
    <g>
      {#each data as point, i}
        {#if point.Label === "Label"}
          <g class="station-tick">
            <text
              x={innerWidth - padding.right}
              y={yScale(i) + barPadding + padding.top + 5}
              text-anchor="start"
            >
              {point["Station Name"]}
            </text>
          </g>
        {/if}
      {/each}
    </g>

    <!-- CREATE THE LINES ON THE LINE GRAPH-->

    {#each data as point, i}
      <!-- Line for 1996 Data-->

      {#if i > 0 && point[variable96] !== null && data[i - 1][variable96] !== null}
        <line
          x1={xScale(data[i - 1][variable96])}
          y1={yScale(i - 1) + barPadding + padding.top}
          x2={xScale(data[i][variable96])}
          y2={yScale(i) + barPadding + padding.top}
          stroke={colour96}
          stroke-width="2"
        />
      {/if}

      <!-- Line for 2021 Data-->
      {#if i > 0 && point[variable21] !== null && data[i - 1][variable21] !== null}
        <line
          x1={xScale(data[i - 1][variable21])}
          y1={yScale(i - 1) + barPadding + padding.top}
          x2={xScale(data[i][variable21])}
          y2={yScale(i) + barPadding + padding.top}
          stroke={colour21}
          stroke-width="2"
        />
      {/if}

      <!-- CREATE THE DOTS ON THE LINE GRAPH-->
      {#if point[variable96] !== null}
        <circle
          class="point"
          r={5}
          cx={xScale(point[variable96])}
          cy={yScale(i) + barPadding + padding.top}
          fill={colour96}
          on:mouseover={(event) => {
            selected_datapoint = point;
            selected_datapoint_i = i;
            setMousePosition(event);
          }}
          on:mouseout={() => {
            selected_datapoint = undefined;
          }}
        />
        <circle
          class="point"
          r={5}
          cx={xScale(point[variable21])}
          cy={yScale(i) + barPadding + padding.top}
          fill={colour21}
          on:mouseover={(event) => {
            selected_datapoint = point;
            selected_datapoint_i = i;
            setMousePosition(event);
          }}
          on:mouseout={() => {
            selected_datapoint = undefined;
          }}
        />



        
      {/if}
    {/each}

    <!-- CITY AVERAGE VALUES-->
    <g>
      <line
        x1={xScale(cityAverage[1][varName])}
        y1={padding.top + 5}
        x2={xScale(cityAverage[1][varName])}
        y2={height}
        stroke={"grey"}
        stroke-width="2"
      />
    </g>

    <!-- X AND Y AXIS-->
    <!-- x axis -->
    <line
      x1={padding.left / 2 - 5}
      y1={padding.top}
      x2={innerWidth}
      y2={padding.top}
      stroke-width={30}
      stroke={lineColour[transitName]}
    />
    {#each xTicks as tick, i}
      <text class="text" x={xScale(tick)} y={padding.top + 5}
        >{thousandToK(tick)}
      </text>
    {/each}
    <!-- y axis -->
    <line
      class="axis y-axis"
      x1={padding.left / 2}
      y1={5}
      x2={padding.left / 2}
      y2={height - padding.bottom-2*barWidth}
      stroke-width={12}
      stroke={lineColour[transitName]}
      z-index="3"
    />

    <!-- CREATE STATION TICKS AND LABELS-->

    <!-- Line that marks the location of the station-->
    <g class="station-lines">
      {#each data as point, i}
        {#if point.Label === "Label" && i + 1 < data.length}
          <line
            class="station-sep-lines"
            x1={innerWidth - padding.right}
            y1={yScale(i) + barPadding + padding.top}
            x2={padding.left}
            y2={yScale(i) + barPadding + padding.top}
            stroke-width={1}
            stroke="#fff"
            stroke-dasharray="5 3"
            opacity="0.5"
          />
          <circle
            class="point"
            r={10}
            cx={padding.left / 2}
            cy={yScale(i) + barPadding + padding.top}
            stroke-width="5px"
            stroke={lineColour[transitName]}
            fill="#FFFFFF"
            on:mouseover={(event) => {
              selected_datapoint = point;
              selected_datapoint_i = i;
              setMousePosition(event);
            }}
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
            opacity="0.5"
          />
          <circle
            class="point"
            r={10}
            cx={padding.left / 2}
            cy={yScale(i) + barPadding + padding.top}
            stroke-width="5px"
            stroke={lineColour[transitName]}
            fill="#FFFFFF"
            on:mouseover={(event) => {
              selected_datapoint = point;
              selected_datapoint_i = i;
              setMousePosition(event);
            }}
          />
        {/if}
      {/each}
    </g>
    {#each data as point, i}
            <!-- CREATE THE BARS ON THE LINE GRAPH-->
            <rect
            class="barLight"
            x={padding.left / 2}
            y={yScale(i) + barWidth / 2 - 2 * barPadding}
            width={0.9*innerWidth - padding.right -20}
            height={barWidth}
            opacity="0"
            on:mouseover={(event) => {
              selected_datapoint = point;
              setMousePosition(event);
              console.log(selected_datapoint);
              document.querySelector(`#var-text-${i}`).style.opacity = 1;
              document.querySelector(`#var-hover-${i}`).style.opacity = 1;
  
              selected_datapoint_i = i;
            }}
            on:mouseout={() => {
              // Reset the opacity of var-text when the mouse leaves the bar
              document.querySelector(`#var-text-${i}`).style.opacity = 0;
              document.querySelector(`#var-hover-${i}`).style.opacity = 0;
  
            }}
          />
          <rect
            class="barLight"
            x={padding.left / 2}
            y={yScale(i) + barWidth / 2 - 2 * barPadding}
            width={xScale(Math.max(point[variable21], point[variable96]))}
            height={barWidth}
            opacity="0.1"
            on:mouseover={(event) => {
              selected_datapoint = point;
              setMousePosition(event);
              console.log(selected_datapoint);
              document.querySelector(`#var-text-${i}`).style.opacity = 1;
              document.querySelector(`#var-hover-${i}`).style.opacity = 1;
  
              selected_datapoint_i = i;
            }}
            on:mouseout={() => {
              // Reset the opacity of var-text when the mouse leaves the bar
              document.querySelector(`#var-text-${i}`).style.opacity = 0;
              document.querySelector(`#var-hover-${i}`).style.opacity = 0;
  
            }}
          />
          <!-- LABELLING THE DATA WILL SHOW ON HOVERING THE BARS-->
        <rect
        id = {`var-hover-${i}`}
        class="var-hover"
        x={0.9*innerWidth-padding.right}
        y={yScale(i) + barWidth / 2 - 2 * barPadding}
        width={500}
        height={barPadding + 3*barWidth}
        opacity="0"
      />
      <text
        id={`var-text-${i}`}
        class="var-text"
        x={0.9*innerWidth - padding.right}
        y={yScale(i) + barPadding + padding.top + 5}
        ><tspan>{point["Station Name"]+": "}</tspan>
        <tspan x={0.9*innerWidth - padding.right + 5} dy={barWidth} dx="1em" fill = {colour96}>{"1996: " + Math.round(point[variable96]*100)/100}</tspan>
        <tspan x={0.9*innerWidth - padding.right + 5} dy={barWidth} dx="1em" fill = {colour21}>{"2021: " + Math.round(point[variable21]*100)/100}</tspan>

      </text>
          {/each}
  </svg>
</div>
<style>
  /* CHART */
  .chart {
    width: 80%;
    left: 0%;
    max-width: 80%;

  }

  svg {
    position: relative;
    width: 80%;
    left: 5%;
  }

  .city-average {
    stroke-width: 2px;
    z-index: 6;
  }
  .city-average-text {
    font-size: 15px;
    fill: #ffffff;
  }

  /* XY axis */
  .text {
    fill: black;
    font-size: 16px;
    background-color: lightgrey;
    font-weight: bold;
  }
  /* RESIZING */
  @media only screen and (max-width: 300px) {
    .chart {
      width: 100%;
      max-width: 100%;
      min-width: 500px;
      margin: 0 auto;
      padding-top: 2%;
    }

  }
  @media only screen and (max-width: 1000px) {
    .chart {
      width: 100%;
      max-width: 100%;
      min-width: 500px;
      margin: 0 auto;
      padding-top: 0%
    }
  }
  svg {
    position: relative;
    width: 100%;
    left: 5%;
  }

  /* AXIS */
  .station-lines {
    stroke-width: 2px;
    z-index: 6;
  }

  .station-tick {
    text-anchor: right;
    fill: var(--brandGray);
    font-size: 17px;
    text-align: right;
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
    stroke: var(--brandWhite);
    fill: var(--brandWhite);
    stroke-opacity: 0.9;
    z-index: 5;
  }

  .barLight:hover {
    opacity: 0.3;
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
    padding-top:5px;
    padding-left:2px;
    fill: #DC4633;
    font-size: 20px;
    font-weight: bold;
  }
  .var-hover{
    fill: black;
  }

</style>
