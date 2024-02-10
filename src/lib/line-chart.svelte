<script>
  import * as d3 from "d3";

  export let title;
  /* data describes an array of objects structured to describe a date and a value
        {
            date,
            value
        }
        */
  export let dataset;

  var transitName = "Line 1: Yonge-University Subway";
  var value = "Population"

  var value96 = value + " 96"
  var value21 = value + " 21"

  //filtre data.json to the selected transitName in page.svelte
  function filterDesignation(dataset) {
    return dataset["Transit Line"] === transitName;
  }

  console.log(transitName);
  var data = dataset.filter(filterDesignation);

  console.log(data);

  // size of the svg
  let width = 2000;
  let height = 1500;
  $: height = Math.min(width / 2.42, 700) + 100;
  const margin = {
    top: 15,
    right: 15,
    bottom: 15,
    left: 15,
  };

  //console.log(data96)
  //Load station names as the xAxis
  const xAxis = []; // all the station names

  for (let i = 0; i < data.length; i++) {
    xAxis.push(data[i]["Station Name"]);
  }
  console.log(xAxis);


  console.log(data, (d) => d["Station Name"]);
  // horizontally create a scale based on the input dates
  const xScale = d3.scaleBand().domain(xAxis).range([0, width]);

  // vertically  consider the input values
  const yScale = d3
    .scaleLinear()
    .domain([0, d3.max(data, (d) => d[value96])])
    // swap [0, height] to have the shapes positioned _from_ the bottom of the svg
    .range([margin.left, width - margin.right]);
  const yScale2 = d3
    .scaleLinear()
    .domain([0, d3.max(data, (d) => d[value21])])
    // swap [0, height] to have the shapes positioned _from_ the bottom of the svg
    .range([height- margin.bottom, margin.top + 0.2 * height]);
  // line function mapping the date and value in the svg
  const line = d3
    .line()
    .x((d) => xScale(d["Station Name"]))
    .y((d) => yScale(d[value96]))
    .curve(d3.curveBundle);
  // second line
  const line2 = d3
    .line()
    .x((d) => xScale(d["Station Name"]))
    .y((d) => yScale2(d[value21]))
    .curve(d3.curveBundle);
  // area function describing the area below the curve described by the dates and values
  const area = d3
    .area()
    .x((d) => xScale(d["Station Name"]))
    .y0((d) => yScale(0))
    .y1((d) => yScale(d[value96]))
    .curve(d3.curveCatmullRom);

  // points highlighted through circle elements
  // in this instance the first and last
  const points = [0, 1, 2, 3, 4, 5, 6];
  var data96 = [];
  var data21 = [];

  for (let point = 0; point < data.length; point++) {
    data96.push({
      x: xScale(data[point]["Station Name"]),
      y: yScale(data[point][value96]),
      value: data[point][value96],
    });

    data21.push({
      x: xScale(data[point]["Station Name"]),
      y: yScale(data[point][value21]),
      value: data[point][value21],
    });
  }


  console.log(data96)
  // "ticks", milestones marked on the x-axis
  // instead of using d3, we create here marks for an arbitrary set of dates
  /*
    const minDate = d3.min(data, d => d["Station Name"]);
    const maxDate = d3.max(data, d => d["Station Name"]);
    const q1 = d3.quantile(data, 0.25, d => d["Station Name"]);
    const q2 = d3.quantile(data, 0.5, d => d["Station Name"]);
    const q3 = d3.quantile(data, 0.75, d => d["Station Name"]);
    */

  
  // "ticks" for the y-axis
  // the idea is to include 10 values, up to the maximum value
  const maxValue = d3.max(data, (d) => d[value96]);
  const yTicks = 10;
  const yAxis = Array(Math.floor(maxValue / yTicks))
    .fill()
    .map((value, index) => (index + 1) * yTicks);

  // variable describing the tooltip
  // the idea is to assign a data point to this variable
  let tooltip = null;

  // subset of the input data delimited by the data points describing an arbitrary start and end
  // the idea is to highlight the specific area through a different visual (in this instance a repeating linear gradient)
  const highlightStart = data.findIndex((d) => d.start);
  const highlightEnd = data.findIndex((d) => d.end);
  const highlight = data.slice(highlightStart, highlightEnd + 1);

  
</script>
<!-- when exiting the article remove the tooltip -->
<!-- when exiting the article remove the tooltip -->
<article
  on:mouseout={() => {
    tooltip = null;
  }}
>
  <h1>{title}</h1>
  <svg
    {width}
    {height}
    viewBox="0 0 {width + (margin.left + margin.right)} {height +
      (margin.top + margin.bottom)}"
  >
    <defs>
      <!-- through a carve out the area dedicated to the data points
            this makes it possible to hide elements behind their circles
            ! use the title in the ID to avoid a conflict between multiple svg
            -->
      <mask id="mask-{title.toLowerCase().split(' ').join('-')}">
        <rect
          x={-margin.left}
          y={-margin.top}
          width={width + (margin.left + margin.right)}
          height={height + (margin.top + margin.bottom)}
          fill="hsl(0, 0%, 100%)"
        />
        {#each data96 as point96}
          <circle
            fill="red"
            stroke="none"
            r="1.5"
            cx={point96.x}
            cy={point96.y}
          />
        {/each}
        {#each data21 as point21}
          <circle
            fill="red"
            stroke="none"
            r="1.5"
            cx={point21.x}
            cy={point21.y}
          />
        {/each}
      </mask>
      <!-- repeating linear gradient describing the highlight section
            ! use the title in the ID to avoid a conflict between multiple svg
             -->
      <linearGradient
        id="gradient-{title.toLowerCase().split(' ').join('-')}"
        gradientUnits="userSpaceOnUse"
        spreadMethod="repeat"
        x1="0"
        x2="1"
        y1="0"
        y2="1"
      >
        <stop stop-color="currentColor" offset="0.5" />
        <stop stop-color="hsl(0, 0%, 100%)" offset="0.5" />
      </linearGradient>
    </defs>
    <g transform="translate({margin.top} {margin.left})">
      <!-- line+area chart
            using the mask to avoid drawing shapes where the highlighted points rest
            -->
      <g mask="url(#mask-{title.toLowerCase().split(' ').join('-')})">
        <!-- area describing the highlight section -->
        <path
          opacity="0.25"
          fill="url(#gradient-{title.toLowerCase().split(' ').join('-')})"
          stroke="none"

        />

        <!-- made-up axes using the dates and values chosen in the Axis variables to draw text and a few lines -->
        <g class="axes">
          <g transform="translate(0 {height})">
            <!-- solid dash of the xAxis -->
            <path
              fill="none"
              stroke="hsl(0, 0%, 0%)"
              stroke-width="0.5"
              d="M 0 0 h {width}"
            />
            {#each xAxis as xTick}
              {console.log(xTick)}
              <g
                transform="translate({xScale(xTick) +
                  xScale.bandwidth() / 2} {height})"
              >
                {console.log(xScale(xTick))}
                <text
                  fill="hsl(0, 0%, 0%)"
                  font-size="6"
                  text-anchor="middle"
                  y="5">{xTick}</text
                >
              </g>
            {/each}
          </g>
          {#each yAxis as yTick}
            <g transform="translate(0 {yScale(yTick)})">
              <!-- grid lines for the y axis -->
              <path
                opacity="0.2"
                fill="none"
                stroke="hsl(0, 0%, 0%)"
                stroke-width="0.5"
                stroke-dasharray="1"
                d="M 0 0 h {width}"
              />
              <!-- position the text right atop the grid lines -->
              <text
                fill="hsl(0, 0%, 0%)"
                opacity="0.5"
                font-size="6"
                text-anchor="start"
                x="0"
                y="-1">{yTick}</text
              >
            </g>
          {/each}
        </g>

        <!-- line chart -->
        <path
          fill="none"
          stroke="currentColor"
          stroke-width="1"
          d={line(data)}
        />
        <path
          fill="none"
          stroke="red"
          stroke-width="1"
          d={line2(data)}
        />

        <!-- area chart -->
        <path opacity="0.15" fill="currentColor" stroke="none" d={area(data)} />
      </g>

      <!-- data points highlighted through circle and text elements -->
      {#each data96 as point96}
        <circle
          fill="none"
          stroke="red"
          stroke-width="1"
          r="1.5"
          cx={point96.x}
          cy={point96.y}
        />
        <text
          text-anchor="middle"
          font-size="10"
          font-weight="bold"
          fill="currentColor"
          x={point96.x}
          y={point96.y - 3}>{point96[value96]}</text
        >
      {/each}
      {#each data21 as point21}
        <circle
          fill="none"
          stroke="red"
          stroke-width="1"
          r="1.5"
          cx={point21.x}
          cy={point21.y}
        />
        <text
          text-anchor="middle"
          font-size="10"
          font-weight="bold"
          fill="currentColor"
          x={point21.x}
          y={point21.y - 3}>{point21[value96]}</text
        >
      {/each}

      <!-- tooltip described with a text, circle, and a line connecting the data point vertically to the x axis -->
      {#if tooltip}
        <g
          fill="currentColor"
          transform="translate({xScale(tooltip["Station Name"])} {yScale(
            tooltip[value96],
          )})"
        >
          <text
            text-anchor="middle"
            font-size="10"
            font-weight="bold"
            fill="hsl(0, 0%, 10%)"
            y="-3">{tooltip[value96]}</text
          >
          <path
            opacity="0.75"
            fill="none"
            stroke="hsl(0, 0%, 10%)"
            stroke-width="0.5"
            stroke-dasharray="1"
            d="M 0 0 v {height - yScale(tooltip[value96])}"
          />
          <circle r="2" fill="hsl(0, 0%, 10%)" />
        </g>
        <g
          fill="currentColor"
          transform="translate({xScale(tooltip["Station Name"])} {yScale(
            tooltip[value21],
          )})"
        >
          <text
            text-anchor="middle"
            font-size="10"
            font-weight="bold"
            fill="hsl(0, 0%, 10%)"
            y="-3">{tooltip[value21]}</text
          >
          <path
            opacity="0.75"
            fill="none"
            stroke="hsl(0, 0%, 10%)"
            stroke-width="0.5"
            stroke-dasharray="1"
            d="M 0 0 v {height - yScale(tooltip[value21])}"
          />
          <circle r="2" fill="hsl(0, 0%, 10%)" />
        </g>
      {/if}

      <!-- rectangles included atop the visualization to manage mouse events  -->
      {#each data as dataPoint, index}
        <g transform="translate({xScale(dataPoint["Station Name"])} 0)">
          <!-- upon entering the rectangle update the tooltip with the data point behind the respective rectangle -->
          <rect
            on:mouseenter={() => {
              tooltip = data[index];
            }}
            opacity="0"
            x="-{xScale(data[1]["Station Name"]) / 2}"
            width={xScale(data[1]["Station Name"]) - xScale(data[0]["Station Name"])}
            {height}
          />
        </g>
      {/each}
    </g>
  </svg>
  <main>
    {#if tooltip}
      <p>{tooltip["Station Name"]} : &nbsp;&nbsp;&nbsp;&nbsp; 1996:&nbsp;&nbsp;{tooltip[value96]} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2021: &nbsp;&nbsp;{tooltip[value21]}</p>
    {/if}
  </main>
</article>

<style>
  svg {
    width: 100%;
    height: auto;
    display: block;
    color: hsl(200, 95%, 45%);
  }
  p {
    font-size: 26px;
    font-style: "red";
  }
</style>