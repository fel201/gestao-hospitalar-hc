import { ref } from "vue";
import { METRICAS_DOCS, type MetricaDoc } from "../data/metricasDocs";

const STORAGE_KEY = "metricas-docs-rascunhos";

type DocComOrigem = MetricaDoc & { nome: string; origem: "codigo" | "rascunho" };

const lerRascunhos = (): Record<string, MetricaDoc> => {
  try {
    const bruto = window.localStorage.getItem(STORAGE_KEY);
    return bruto ? JSON.parse(bruto) : {};
  } catch {
    return {};
  }
};

const escreverRascunhos = (dados: Record<string, MetricaDoc>) => {
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(dados));
};

// Estado reativo compartilhado entre todas as instâncias que usarem o composable
// (garante que a lista se atualize sozinha assim que algo for salvo/excluído).
const rascunhos = ref<Record<string, MetricaDoc>>(lerRascunhos());

export function useMetricasDocs() {
  const listar = (): DocComOrigem[] => {
    const nomes = new Set([
      ...Object.keys(METRICAS_DOCS),
      ...Object.keys(rascunhos.value),
    ]);

    return Array.from(nomes).map((nome) => {
      const temRascunho = nome in rascunhos.value;
      const doc = temRascunho ? rascunhos.value[nome] : METRICAS_DOCS[nome];
      return { nome, ...doc, origem: temRascunho ? "rascunho" : "codigo" } as DocComOrigem;
    });
  };

  const obter = (nome: string): DocComOrigem | null => {
    const temRascunho = nome in rascunhos.value;
    const doc = temRascunho ? rascunhos.value[nome] : METRICAS_DOCS[nome];
    if (!doc) return null;
    return { nome, ...doc, origem: temRascunho ? "rascunho" : "codigo" };
  };

  const salvar = (nome: string, doc: MetricaDoc) => {
    rascunhos.value = { ...rascunhos.value, [nome]: doc };
    escreverRascunhos(rascunhos.value);
  };

  // Só remove o rascunho local. Uma doc que já existe no código volta a
  // mostrar a versão do código — não some, porque essa fonte não é editável
  // por aqui.
  const descartarRascunho = (nome: string) => {
    const copia = { ...rascunhos.value };
    delete copia[nome];
    rascunhos.value = copia;
    escreverRascunhos(copia);
  };

  const temRascunhos = () => Object.keys(rascunhos.value).length > 0;

  // Gera o objeto TS pronto pra colar em METRICAS_DOCS, no metricasDocs.ts.
  const exportarComoCodigo = (): string => {
    const entradas = Object.entries(rascunhos.value)
      .map(([nome, doc]) => {
        const linhas = [
          `  "${nome.replace(/"/g, '\\"')}": {`,
          `    titulo: ${JSON.stringify(doc.titulo)},`,
          `    modulo: ${JSON.stringify(doc.modulo)},`,
          `    calculo: ${JSON.stringify(doc.calculo)},`,
        ];
        linhas.push("  },");
        return linhas.join("\n");
      })
      .join("\n");

    return `{\n${entradas}\n}`;
  };

  return { listar, obter, salvar, descartarRascunho, temRascunhos, exportarComoCodigo };
}