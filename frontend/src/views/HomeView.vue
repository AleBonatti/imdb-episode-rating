<script setup>
import { ref } from 'vue';
import VueApexCharts from "vue3-apexcharts";

let text = ref('');
let series = ref(null);
let selectedSerie = ref(null);
let selectedStagione = ref(null);
let details = ref(null);
let searching = ref(false);
let showGraph = ref(false);
let title = ref('Home');

// dati graph
let chartOptions = ref({});
let dati = ref([]);

let search = () => {
    title.value = 'Home';
    if(series.value!==null) series.value = null;
    if(selectedSerie.value!==null) selectedSerie.value = null;
    if(selectedStagione.value!==null) selectedStagione.value = null;
    if(showGraph.value) showGraph.value = false;
    searching.value = true;

    axios.get('http://127.0.0.1:8000/search', { params: { text: text.value }})
        .then(response => {
            series.value = response.data.results;
        })
        .catch(error => {
            alert('error');
            console.log(error.response);
        })
        .then(response => {
            searching.value = false;
        });
}

let getDetails = (id) => {
    if(showGraph.value) showGraph.value = false;
    if(details.value!==null) details.value = null;
    
    selectedSerie.value = id;
    setTimeout(function() {
        axios.get(`http://127.0.0.1:8000/details/${id}`)
            .then(response => {
                details.value = response.data;
                title.value = details.value.title;
            })
            .catch(error => {
                alert('error');
                console.log(error.response);
            });
    }, 800);
}

let getSeason = (id, stagione) => {
    selectedStagione.value = stagione;
    title.value = `${details.value.title} - stagione ${stagione}`;
    axios.get(`http://127.0.0.1:8000/episodes/${id}/${stagione}`)
        .then(response => {
            let episodes = response.data.episodes;

            chartOptions.value = {
                chart: { id: "vuechart-example" },
                xaxis: {
                    categories: episodes.map(a => a.title)
                }
            }

            dati.value = [{
                name: 'Rate Imdb',
                data: episodes.map(a => a.imDbRating)
            }];

            series.value = null;
            text.value = '';
            showGraph.value = true;
        })
        .catch(error => {
            alert('error');
            console.log(error);
        });
}

let fetchSeason = (ev) => {
    console.log(selectedSerie.value, ev.target.value);
    getSeason(selectedSerie.value, ev.target.value);
}
</script>

<template>
    <main>
        <h1>{{ title }}</h1>
        
        <div class="w-1/2 mt-8 m-auto">
            <div class="flex rounded-md shadow-sm">
                <div class="relative flex flex-grow items-stretch focus-within:z-10">
                    <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center pl-3 text-gray-500">
                        <svg v-if="searching" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5 animate-spin mr-2">
                            <path fill-rule="evenodd" d="M4.755 10.059a7.5 7.5 0 0112.548-3.364l1.903 1.903h-3.183a.75.75 0 100 1.5h4.992a.75.75 0 00.75-.75V4.356a.75.75 0 00-1.5 0v3.18l-1.9-1.9A9 9 0 003.306 9.67a.75.75 0 101.45.388zm15.408 3.352a.75.75 0 00-.919.53 7.5 7.5 0 01-12.548 3.364l-1.902-1.903h3.183a.75.75 0 000-1.5H2.984a.75.75 0 00-.75.75v4.992a.75.75 0 001.5 0v-3.18l1.9 1.9a9 9 0 0015.059-4.035.75.75 0 00-.53-.918z" clip-rule="evenodd" />
                        </svg>
                    </div>
                    <input type="text" v-model="text" placeholder="cerca una serie" class="block w-full rounded-none rounded-l-md border-0 py-1.5 px-3 pr-10 text-gray-900 ring-1 ring-gray-300 ring-inset placeholder:text-gray-400 focus:ring-1 focus:ring-gray-600 focus:ring-inset sm:text-sm sm:leading-6" />
                </div>
                <button type="button" @click="search" :disabled="searching" class="disabled:opacity-75 relative -ml-px inline-flex bg-gray-700 items-center gap-x-1.5 rounded-r-md px-3 py-2 text-sm text-gray-200 ring-1 ring-inset ring-gray-600 hover:bg-gray-800">
                    Search
                </button>
            </div>

            <div v-if="series!==null">
                <ul v-if="series.length" role="list" class="divide-y divide-gray-100">
                    <li v-for="serie in series" :key="serie.id" class="py-5">
                        <div class="flex items-center justify-between gap-x-6 ">
                            <div class="flex gap-x-4">
                                <img v-if="serie.image!==''" class="h-12 w-12 flex-none rounded-full bg-gray-50" :src="serie.image" alt="" />
                                <span v-else class="inline-block h-12 w-12 overflow-hidden rounded-full bg-gray-100">
                                    <svg class="h-full w-full text-gray-300" fill="currentColor" viewBox="0 0 24 24">
                                        <path d="M24 20.993V24H0v-2.996A14.977 14.977 0 0112.004 15c4.904 0 9.26 2.354 11.996 5.993zM16.002 8.999a4 4 0 11-8 0 4 4 0 018 0z" />
                                    </svg>
                                </span>
                                <div class="min-w-0">
                                    <p class="text-sm font-semibold leading-6 text-gray-900">{{ serie.title }}</p>
                                    <p class="mt-1 truncate text-xs leading-5 text-gray-500">{{ serie.description }}</p>
                                </div>
                            </div>
                            <a href="#" @click.prevent="getDetails(serie.id)" class="rounded-full bg-white px-2.5 py-1 text-xs font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">Dettagli</a>
                        </div>
                        <div v-if="selectedSerie===serie.id" class="rounded-md border border-gray-300 p-4 mt-4 text-gray-500">
                            <svg v-if="details===null" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="m-auto w-5 h-5 animate-spin">
                                <path fill-rule="evenodd" d="M4.755 10.059a7.5 7.5 0 0112.548-3.364l1.903 1.903h-3.183a.75.75 0 100 1.5h4.992a.75.75 0 00.75-.75V4.356a.75.75 0 00-1.5 0v3.18l-1.9-1.9A9 9 0 003.306 9.67a.75.75 0 101.45.388zm15.408 3.352a.75.75 0 00-.919.53 7.5 7.5 0 01-12.548 3.364l-1.902-1.903h3.183a.75.75 0 000-1.5H2.984a.75.75 0 00-.75.75v4.992a.75.75 0 001.5 0v-3.18l1.9 1.9a9 9 0 0015.059-4.035.75.75 0 00-.53-.918z" clip-rule="evenodd" />
                            </svg>
                            <div v-else-if="details.tvSeriesInfo">
                                <ul>
                                    <li v-for="stagione in details.tvSeriesInfo.seasons" :key="stagione">
                                        <a href="#" @click.prevent="getSeason(serie.id, stagione)">Stagione {{ stagione }}</a>
                                    </li>
                                </ul>
                            </div>
                            <div v-else>
                                Stagioni non disponibili
                            </div>
                        </div>
                    </li>
                </ul>
                <div v-else class="rounded-md mt-6 bg-red-100 p-4">
                    <div class="flex">
                        <h3 class="text-sm font-medium text-red-800">Nessun risultato trovato per {{ text }}</h3>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="showGraph" class="mt-8">
            <div>
                <select v-model="selectedStagione" @change="fetchSeason($event)" class="mt-2 block rounded-md border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6">
                    <option v-for="stagione in details.tvSeriesInfo.seasons" :key="stagione" :value="stagione">stagione {{ stagione }}</option>
                </select>
            </div>
            <vue-apex-charts width="100%" type="bar" :options="chartOptions" :series="dati" />
        </div>
    </main>
</template>