<script>
  import { scaleLinear } from "d3-scale"; // for scaling data to graph the data points
  import jsondata from "../data/data.json"; // import data
  import { onMount, onDestroy } from "svelte";
  import "../assets/global-styles.css";
  import cityAverage from "../data/cdData.json";

  //export let data;
  export let variable96; //get the selected variable name for 2021
  export let variable21; //get the selected variable name for 2021
  export let colour96; // set colour for 1996
  export let colour21; // set colour for 2021
  export let maxHeight; //
  export let transitName;

  /* ======= SETTING UP DATA ==========*/

  //filtre data.json to the selected transitName in page.svelte
  function filterDesignation(jsondata) {
    return jsondata["Transit Line"] === transitName;
  }
  // store filtered jsondata in variable called data
  var data = jsondata.filter(filterDesignation);

  /* ======= SETTING UP CHARTING AREAS ==========*/
  const padding = { top: 20, right: 60, bottom: 10, left: 15 };
  let width = 800; // set the base width
  let height = data.length * 5 + padding.top + padding.bottom; // set the base width

  // adjust the width of the graph based on viewing size
  $: innerWidth = width - (padding.left + padding.right);
  $: innerHeight = height - (padding.top + padding.bottom);
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
  var xTicks = [];
  for (let i = 0; i <= roundedValue; i += interval) {
    xTicks.push(Math.round(i));
  }
  console.log(xTicks);

  // converts thousands and million to K and M i.e. (1,000 ==> 1K , 1,000,000 ==> 1M)
  function thousandToK(tick) {
    var newtick;
    if (tick >= 1000 && tick < 1000000) {
      newtick = tick / 1000 + "K";
    } else if (tick > 1000000) {
      newtick = tick / 1000000 + "M";
    } else {
      newtick = tick;
    }
    return newtick;
  }

  /* ======= SCALING DATA POINTS ========== */
  $: xScale = scaleLinear()
    .domain([0, xTicks.length])
    .range([padding.left, width - padding.right]);

  $: yScale = scaleLinear()
    .domain([0, Math.max.apply(null, yTicks)])
    .range([padding.top, height - padding.bottom]); // added 0.2*height to accomodate station text label.

  // ------SETTING UP BARS FOR THE BAR CHART ------------------------
  var barPadding = 10; // controls how much spacing the bars will be from the
  // control barwidth based on viewing window width
  $: barWidth = Math.max(Math.min(innerHeight / yTicks.length, 25), 6);

  /* ======= SET UP DATA LABELLING ========== */
  let selected_datapoint = undefined;
  let selected_datapoint_i = undefined;

  // NOT SURE WHAT THIS IS FOR, REMOVE IF UNNECESSARY
  var varName = variable96.replace(" 96", "").replace("Weighted ", "");
</script>

<div id="barchart" class="chart" bind:clientHeight={height}>
  <svg
    height={data.length * (barWidth + barPadding) +
      padding.top +
      padding.bottom}
  >
    <!-- CREATE STATION TICKS AND LABELS-->
    <g class="station-lines">
      {#each data as point, i}
        {#if point.Label === "Label" && i + 1 < data.length}
          <line
            class="station-sep-lines"
            x1={width - padding.right}
            y1={yScale(i) + barPadding}
            x2={padding.left}
            y2={yScale(i) + barPadding}
            stroke-width={1}
            stroke="#fff"
            stroke-dasharray="5 3"
            opacity="0.5"
          />
          <circle
            class="point"
            r={innerWidth / 300}
            cx={width - padding.right}
            cy={yScale(i) + barPadding}
            stroke-width="2px"
            stroke="#FFFFFF"
            fill="#000000"
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
            x1={width - padding.right}
            y1={yScale(i) + barPadding}
            x2={padding.left}
            y2={yScale(i) + barPadding}
            stroke-width={1}
            stroke="#fff"
            stroke-dasharray="5 3"
            opacity="0.5"
          />
          <circle
            class="point"
            r={innerWidth / 300}
            cx={width - padding.right}
            cy={yScale(i) + barPadding}
            stroke-width="2px"
            stroke="red"
            fill="#000000"
            on:mouseover={(event) => {
              selected_datapoint = point;
              selected_datapoint_i = i;
              setMousePosition(event);
            }}
          />
        {/if}
      {/each}
    </g>
    <!-- TEXT LABEL FOR THE STATION NAMES-->
    <g>
      {#each data as point, i}
        {#if point.Label === "Label"}
          <g class="station-tick">
            <text
              x={width - padding.right + 10}
              y={yScale(i) + barPadding + 5}
              text-anchor="start"
            >
              {point["Station Name"]}
            </text>
          </g>
        {/if}
      {/each}
    </g>
    <!-- y axis -->
    <g class="axis x-axis">
      {#each xTicks as tick}
      {console.log(tick)}
      {console.log(xScale(tick))}
        <g class="tick tick-{tick}">
          <line x1="60%" stroke-width="10" />
          <text x={xScale(tick)} y={padding.top}>{thousandToK(tick)} </text>
        </g>
      {/each}
    </g>
    <!-- the lines and circles of the line chart  -->
    <g>
      {#each data as point, i}
        <!-- Line for 1996 Data-->

        {#if i > 0 && point[variable96] !== null && data[i - 1][variable96] !== null}
          <line
            x1={xScale(data[i - 1][variable96])}
            y1={yScale(i - 1) + barPadding + barWidth / 2 - 1}
            x2={xScale(data[i][variable96])}
            y2={yScale(i) + barPadding + barWidth / 2 - 1}
            stroke={colour96}
            stroke-width="2"
          />
        {/if}

        <!-- Line for 2021 Data-->
        {#if i > 0 && point[variable21] !== null && data[i - 1][variable21] !== null}
          <line
            x1={xScale(i - 1) + barPadding + barWidth / 2 - 1}
            y1={yScale(data[i - 1][variable21])}
            x2={xScale(i) + barPadding + barWidth / 2 - 1}
            y2={yScale(point[variable21])}
            stroke={colour21}
            stroke-width="2"
          />
        {/if}
        {#if point[variable96] !== null}
          {console.log(xScale(point[variable96]) / 10000)}
          <circle
            class="point"
            r={5}
            cx={xScale(point[variable96]) / 10000 + padding.left}
            cy={padding.top * 3}
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
            r={innerWidth / 400}
            cx={xScale(i) + barPadding + barWidth / 2 - 1}
            cy={yScale(point[variable21])}
            fill={colour21}
            on:mouseover={(event) => {
              selected_datapoint = point;
              selected_datapoint_i = i;
              setMousePosition(event);
            }}
          />
          <rect
            class="barLight"
            x={xScale(Math.max(point[variable21], point[variable96]))}
            y={xScale(i) + barPadding}
            width={barWidth - 2}
            height={xScale(0) -
              xScale(Math.max(point[variable21], point[variable96]))}
            stroke={"greu"}
            opacity="0.15"
            on:mouseover={(event) => {
              selected_datapoint = point;
              setMousePosition(event);
              selected_datapoint_i = i;
            }}
          />
        {/if}
      {/each}
    </g>
  </svg>
</div>

<style>
  /* CHART */
  .chart {
    width: 90%;
    max-width: 100%;
    min-width: 500px;
    margin: 0 auto;
    padding-top: 1%;
  }

  svg {
    position: relative;
    width: 100%;
  }

  .city-average {
    stroke-width: 2px;
    z-index: 6;
  }
  .city-average-text {
    font-size: 15px;
    fill: #ffffff;
  }

  /* RESIZING */
  @media only screen and (max-width: 300px) {
    .chart {
      width: 96%;
      max-width: 100%;
      min-width: 500px;
      margin: 0 auto;
      padding-top: 2%;
    }
    #hoverLabel p {
      color: var(--brandWhite);
      font-family: RobotoRegular;
      font-size: 10px;
      text-align: center;
    }
  }
  @media only screen and (max-width: 1258px) {
    .chart {
      width: 90%;
      max-width: 100%;
      min-width: 500px;
      margin: 0 auto;
      padding-top: 0%;
    }
  }

  /* AXIS */
  .year-tick {
    stroke-width: 2px;
    z-index: 6;
  }
  .station-lines {
    stroke-width: 2px;
    z-index: 6;
  }
  .tick {
    font-family: RobotoRegular;
    font-size: 0.725em;
    font-weight: 200;
  }

  .tick line {
    stroke: var(--brandGray);
    stroke-width: 1px;
    opacity: 0.1;
    padding: 10%;
  }
  /* controls the styling for all tick texts */
  .tick text {
    fill: var(--brandGray);
    text-anchor: start;
    font-size: 16px;
  }

  .tick.tick-0 line {
    stroke-dasharray: 0;
  }

  .y-axis .tick text {
    text-anchor: middle;
    font-size: 15px;
    text-align: left;
  }
  .y-label {
    text-anchor: middle;
    transform: translate(-10px, 0px) rotate(-45deg);
  }

  .y-label.tick text {
    font-size: 15px;
    fill: #000000;
  }
  .station-tick {
    text-anchor: right;
    fill: var(--brandGray);
    font-size: 15px;
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
  .bar {
    stroke: var(--brandDarkGreen);
    stroke-width: 1px;
    stroke-opacity: 1;
    fill: var(--brandWhite);
    cursor: pointer;
  }

  .bar:hover {
    fill: var(--brandLightBlue);
    opacity: 1;
  }

  .barLight {
    stroke: var(--brandDarkGreen);
    stroke-width: 1px;
    stroke-opacity: 1;
    fill: var(--brandWhite);
  }

  .barLight:hover {
    opacity: 0.4;
    cursor: pointer;
  }

  /* HOVERING */
  #hoverLabel {
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  #hoverLabel p {
    color: var(--brandWhite);
    font-family: RobotoRegular;
    font-size: 15px;
    text-align: center;
  }
  .tip {
    stroke: var(--brandDarkGreen);
    stroke-width: 1px;
    fill: var(--brandYellow);
  }
</style>
