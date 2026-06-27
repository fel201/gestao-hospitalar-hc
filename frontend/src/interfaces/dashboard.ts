export interface DashboardInterface {
  especialidade: string;
  kpis: DashboardKPIsInterface;
  etapas: DashboardEtapaInterface[];
}

export interface DashboardKPIsInterface {
  total_pacientes: number;
  total_eventos: number;
  tempo_medio_jornada: number;
  taxa_conclusao: number;
}

export interface DashboardEtapaInterface {
  id: string;
  titulo: string;
  total_eventos?: number;
  eventos?: DashboardEventoInterface[];
  indicadores?: DashboardIndicadorInterface[];
}

export interface DashboardEventoInterface {
  nome: string;
  valor: number;
}

export interface DashboardIndicadorInterface {
  nome: string;
  valor: number;
}