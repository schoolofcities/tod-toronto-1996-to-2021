<script>
    export let chartWidth;
    export let chartHeight;

    const paddings = {
        top: 50,
        left: 50, 
        right: 50,
        bottom: 50,
    };

</script>

<svg width = {chartWidth} height = {chartHeight}>
<g>
    <line 
        x1 = {paddings.left}
        x2 = {chartWidth - paddings.right}
        y1 = {chartHeight - paddings.bottom}
        y2 = {chartHeight - paddings.bottom}
        stroke = "black"
        stroke-width = "2" />

        

</g>
</svg>