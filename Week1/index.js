const axios = require('axios');

const apiConfigs = [
    { name: "GitHub", url: "https://api.github.com/users/octocat", headers: { 'User-Agent': 'Nodejs' } },
    { name: "JSONPlaceholder", url: "https://jsonplaceholder.typicode.com/posts/1", headers: {} },
    { name: "PokeAPI", url: "https://pokeapi.co/api/v2/pokemon/pikachu", headers: {} }
];

async function runAnalysis() {
    const rawResponses = await Promise.all(apiConfigs.map(api =>
        axios.get(api.url, { headers: api.headers }).catch(err => ({ error: err.message }))
    ));

    const finalReport = rawResponses.map((res, index) => {
        if (res.error) return { api: apiConfigs[index].name, status: "Failed", message: res.error };

        const data = res.data;

        return {
            api: apiConfigs[index].name,
            status: res.status,
            dataSummary: Object.keys(data).slice(0, 3).reduce((obj, key) => {
                obj[key] = data[key];
                return obj;
            }, {}),
            endpoint: apiConfigs[index].url
        };
    });

    console.log(JSON.stringify(finalReport, null, 2));
}

runAnalysis();