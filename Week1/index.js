const axios = require('axios');

const apiConfigs = [
    { name: "GitHub", url: "https://api.github.com/users/octocat", headers: { 'User-Agent': 'Nodejs' } },
    { name: "JSONPlaceholder", url: "https://jsonplaceholder.typicode.com/posts/1", headers: {} },
    { name: "PokeAPI", url: "https://pokeapi.co/api/v2/pokemon/pikachu", headers: {} }
];

async function runAnalysis() {
    // Gọi tất cả API song song
    const rawResponses = await Promise.all(apiConfigs.map(api =>
        axios.get(api.url, { headers: api.headers }).catch(err => ({ error: err.message }))
    ));

    // Logic xử lý động (Dynamic Parsing) - Không hard-code tên thuộc tính
    const finalReport = rawResponses.map((res, index) => {
        if (res.error) return { api: apiConfigs[index].name, status: "Failed", message: res.error };

        const data = res.data;

        return {
            api: apiConfigs[index].name,
            status: res.status,
            // Tự động lấy 3 key đầu tiên của JSON trả về để phân tích mẫu
            dataSummary: Object.keys(data).slice(0, 3).reduce((obj, key) => {
                obj[key] = data[key];
                return obj;
            }, {}),
            endpoint: apiConfigs[index].url
        };
    });

    // CHỈ dùng duy nhất 1 console.log và JSON.parse/stringify
    console.log(JSON.stringify(finalReport, null, 2));
}

runAnalysis();