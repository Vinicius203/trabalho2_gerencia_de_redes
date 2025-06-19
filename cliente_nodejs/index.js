const axios = require('axios');

const flaskApiBaseUrl = 'http://localhost:5000';

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function executarTarefaLonga() {
    console.log('🚀 1. Solicitando o início da tarefa de scraping para gerar o CSV...');

    try {
        const startResponse = await axios.post(`${flaskApiBaseUrl}/iniciar-tarefa`);
        const { task_id, status_url } = startResponse.data;
        console.log(`✅ Tarefa iniciada com ID: ${task_id}`);
        console.log('\n🔄 2. Verificando o status da tarefa a cada 5 segundos...');

        let statusData;
        while (true) {
            const statusResponse = await axios.get(status_url);
            statusData = statusResponse.data;
            console.log(`   - Status atual: ${statusData.status}`);
            if (statusData.status === 'concluido' || statusData.status === 'erro') break;
            await sleep(5000);
        }

        console.log('\n🏁 3. Tarefa finalizada!');
        if (statusData.status === 'concluido') {
            const { mensagem, nome_arquivo, url_download } = statusData.resultado;
            console.log('✅ Sucesso!');
            console.log(`   - Mensagem: ${mensagem}`);
            console.log(`   - Arquivo: ${nome_arquivo}`);
            console.log(`   - Baixe seu relatório aqui: ${url_download}`);
        } else {
            console.error('❌ A tarefa falhou:', statusData.resultado);
        }

    } catch (error) {
        console.error('\n❌ Ocorreu um erro durante o processo:', error.message);
    }
}

executarTarefaLonga();

