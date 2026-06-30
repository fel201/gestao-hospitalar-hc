export interface DashboardInterface {
  especialidade: string;
  kpis: DashboardKPIsInterface;
  entrada: DashboardModuloInterface;
  consultas: DashboardModuloInterface;
  exames: DashboardModuloInterface;
  internacao: DashboardModuloInterface;
  cirurgias: DashboardModuloInterface;
}

export interface DashboardKPIsInterface {
  total_pacientes: number;
  total_eventos: number;
  tempo_medio_jornada: number;
  taxa_conclusao: number;
}

export interface DashboardModuloInterface {
  titulo: string;
  total_eventos: number;
  eventos: DashboardEventoInterface[];
  indicadores: DashboardIndicadorInterface[];
}

export interface DashboardEventoInterface {
  nome: string;
  valor: number;
}

// cada KPI de cada módulo vai ser adicionada aqui blz
export interface DashboardIndicadorInterface {
  nome: string;
  valor: number;
}
