<template>
  <div class="search-container">
    <h1>Busca de Operadoras de Saúde</h1>

    <div class="search-box">
      <input
        type="text"
        v-model="searchQuery"
        @input="handleInput"
        placeholder="Digite nome, CNPJ, cidade..."
      />
      <button @click="searchOperadoras">Buscar</button>
    </div>

    <div v-if="loading" class="loading">Carregando...</div>

    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="results.length > 0" class="results-container">
      <div class="results-count">
        {{ results.length }} resultados encontrados
      </div>

      <div class="result-item" v-for="(item, index) in results" :key="index">
        <h3>{{ item.Nome_Fantasia || item.Razao_Social }}</h3>
        <p><strong>CNPJ:</strong> {{ item.CNPJ }}</p>
        <p><strong>Registro ANS:</strong> {{ item.Registro_ANS }}</p>
        <p><strong>Cidade/UF:</strong> {{ item.Cidade }}/{{ item.UF }}</p>
        <p><strong>Modalidade:</strong> {{ item.Modalidade }}</p>
        <div class="more-info" v-if="expandedItems.includes(index)">
          <p>
            <strong>Endereço:</strong> {{ item.Logradouro }},
            {{ item.Numero }} - {{ item.Bairro }}
          </p>
          <p><strong>Telefone:</strong> ({{ item.DDD }}) {{ item.Telefone }}</p>
          <p><strong>Email:</strong> {{ item.Endereco_eletronico }}</p>
        </div>
        <button @click="toggleExpand(index)" class="expand-btn">
          {{ expandedItems.includes(index) ? "Mostrar menos" : "Mostrar mais" }}
        </button>
      </div>
    </div>

    <div v-else-if="searchPerformed" class="no-results">
      <template v-if="searchQuery.trim()">
        Nenhum resultado encontrado para "{{ searchQuery }}"
      </template>
      <template v-else> Por favor, digite um termo para buscar </template>
    </div>
  </div>
</template>

<script>
import _ from "lodash";
import axios from "axios";

export default {
  name: "SearchOperadoras",
  data() {
    return {
      searchQuery: "",
      results: [],
      loading: false,
      error: "",
      searchPerformed: false,
      expandedItems: [],
    };
  },
  methods: {
    handleInput: _.debounce(function () {
      if (this.searchQuery.trim()) {
        this.searchOperadoras();
      }
    }, 500),

    async searchOperadoras() {
      if (!this.searchQuery.trim()) {
        this.error = "Por favor, digite um termo para buscar";
        this.results = [];
        this.searchPerformed = true;
        return;
      }

      this.loading = true;
      this.error = "";
      this.searchPerformed = true;

      try {
        const response = await axios.get(`http://localhost:5000/api/search`, {
          params: { q: this.searchQuery.trim() },
        });

        if (response.data.error) {
          throw new Error(response.data.message || response.data.error);
        }

        this.results = response.data;
        this.expandedItems = [];

        if (this.results.length === 0) {
          this.error = `Nenhum resultado encontrado para "${this.searchQuery}"`;
        }
      } catch (err) {
        console.error("Erro completo:", err);
        if (err.response) {
          this.error =
            err.response.data.message ||
            err.response.data.error ||
            "Erro ao processar sua requisição";
        } else {
          this.error = err.message || "Erro ao conectar com o servidor";
        }
        this.results = [];
      } finally {
        this.loading = false;
      }
    },

    toggleExpand(index) {
      if (this.expandedItems.includes(index)) {
        this.expandedItems = this.expandedItems.filter((i) => i !== index);
      } else {
        this.expandedItems.push(index);
      }
    },
  },
};
</script>

<style scoped>
.search-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.search-box {
  display: flex;
  margin: 20px 0;
}

.search-box input {
  flex: 1;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px 0 0 4px;
}

.search-box button {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
}

.result-item {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 15px;
}

.result-item h3 {
  margin-top: 0;
  color: #2c3e50;
}

.expand-btn {
  background: none;
  border: none;
  color: #42b983;
  cursor: pointer;
  padding: 5px 0;
}

.more-info {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px dashed #eee;
}

.loading,
.error,
.no-results {
  text-align: center;
  padding: 20px;
  color: #666;
}

.error {
  color: #e74c3c;
}

.results-count {
  margin-bottom: 15px;
  font-style: italic;
  color: #666;
}
</style>
