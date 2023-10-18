<script>
    import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

    onMount(() => {
        goto('/transit-analysis/growth');
    });

</script>

Hello World!