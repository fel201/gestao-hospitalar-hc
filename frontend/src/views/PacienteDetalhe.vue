<template>
  <div class="min-h-screen bg-slate-900 text-slate-200 p-6">

    <!-- ==========================================
         TELA DE CARREGAMENTO
         ========================================== -->
    <div v-if="carregando" class="flex flex-col items-center justify-center min-h-[80vh] space-y-8">
      
      <!-- Logo/Ícone animado -->
      <div class="relative">
        <div class="w-24 h-24 rounded-full bg-blue-500/10 border-4 border-blue-500/30 flex items-center justify-center animate-pulse">
          <svg class="w-12 h-12 text-blue-400 animate-spin-slow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        
        <!-- Anel de carregamento externo -->
        <div class="absolute inset-0 rounded-full border-t-4 border-blue-400 animate-spin"></div>
        <div class="absolute inset-0 rounded-full border-r-4 border-purple-400 animate-spin-reverse"></div>
      </div>

      <!-- Texto de carregamento -->
      <div class="text-center space-y-3">
        <h2 class="text-2xl font-bold text-white">
          Carregando Jornada do Paciente
        </h2>
        <p class="text-slate-400 text-sm">
          Buscando informações clínicas e histórico de atendimentos...
        </p>
      </div>

      <!-- Barra de progresso animada -->
      <div class="w-64 h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div class="h-full bg-linear-to-r from-blue-500 via-purple-500 to-blue-500 rounded-full animate-progress"></div>
      </div>

      <!-- Dicas de carregamento -->
      <div class="mt-4 max-w-md text-center">
        <p class="text-xs text-slate-500 animate-pulse">
          <span class="inline-block mr-2">⏳</span>
          {{ dicaAtual }}
        </p>
      </div>

      <!-- Indicador de etapas -->
      <div class="flex items-center gap-3 mt-2">
        <div v-for="i in 4" :key="i" class="flex items-center">
          <div 
            class="w-2 h-2 rounded-full transition-colors duration-300"
            :class="i <= etapaAtual ? 'bg-blue-400' : 'bg-slate-700'"
          ></div>
          <div v-if="i < 4" class="w-4 h-px" :class="i < etapaAtual ? 'bg-blue-400/30' : 'bg-slate-700'"></div>
        </div>
      </div>

    </div>

    <!-- ==========================================
         CONTEÚDO PRINCIPAL
         ========================================== -->
    <template v-else>

      <!-- ANDAR SUPERIOR: Cabeçalho e Métricas -->
      <div class="mb-8 space-y-4">

        <!-- Card de identidade do paciente -->
        <Card class="bg-slate-800 border-slate-700 p-6 relative">
          <h1 class="text-2xl font-bold text-white mb-1">DETALHES DA JORNADA DO PACIENTE</h1>
          <p class="text-sm text-slate-400 mb-6">Hospital das Clínicas - Perspectiva do Paciente</p>

          <div class="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm">
            <div class="flex items-center gap-3">
              <div class="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center text-white">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <div>
                <div class="text-slate-400 text-xs">Paciente</div>
                <div class="font-medium text-white">{{ jornada?.paciente?.nome ?? 'Carregando...' }}</div>
              </div>
            </div>

            <div>
              <div class="text-slate-400 text-xs">Prontuário</div>
              <div class="font-medium text-white">{{ jornada?.paciente?.prontuario ?? '—' }}</div>
            </div>

            <div>
              <div class="text-slate-400 text-xs">Diagnóstico</div>
              <div class="font-medium text-white">Insuficiência Cardíaca Congestiva</div>
            </div>

            <div>
              <div class="text-slate-400 text-xs">CID</div>
              <div class="font-medium text-white">I50.0</div>
            </div>
          </div>
        </Card>

        <!-- Cards de métricas -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">

          <Card class="bg-slate-800 border-slate-700 py-4 px-5">
            <div class="flex items-center gap-4">
              <div class="p-3 bg-slate-900 rounded-lg text-blue-500">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-slate-400">Total de Eventos</p>
                <p class="text-xl font-bold text-white">{{ jornada?.metricas?.numero_eventos ?? '—' }}</p>
              </div>
            </div>
          </Card>

          <Card class="bg-slate-800 border-slate-700 py-4 px-5">
            <div class="flex items-center gap-4">
              <div class="p-3 bg-slate-900 rounded-lg text-yellow-500">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-slate-400">Exames Realizados</p>
                <p class="text-xl font-bold text-white">{{ jornada?.metricas?.numero_exames ?? '—' }}</p>
              </div>
            </div>
          </Card>

          <Card class="bg-slate-800 border-slate-700 py-4 px-5">
            <div class="flex items-center gap-4">
              <div class="p-3 bg-slate-900 rounded-lg text-emerald-500">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-slate-400">Consultas</p>
                <p class="text-xl font-bold text-white">{{ jornada?.metricas?.numero_consultas ?? '—' }}</p>
              </div>
            </div>
          </Card>

          <Card class="bg-slate-800 border-slate-700 py-4 px-5">
            <div class="flex items-center gap-4">
              <div class="p-3 bg-slate-900 rounded-lg text-indigo-400">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-slate-400">Dias de Internação</p>
                <p class="text-xl font-bold text-white">{{ jornada?.metricas?.numero_internacoes ?? '—' }}</p>
              </div>
            </div>
          </Card>

          <Card class="bg-slate-800 border-slate-700 py-4 px-5">
            <div class="flex items-center gap-4">
              <div class="p-3 bg-slate-900 rounded-lg text-orange-500">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2a1 1 0 01-.293.707L13 13.414V19a1 1 0 01-.553.894l-4 2A1 1 0 017 21v-7.586L3.293 6.707A1 1 0 013 6V4z" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-slate-400">Filtro Ativo</p>
                <p class="text-sm font-bold text-white">
                  {{ jornada?.metricas?.filtro_especificacao?.length
                      ? jornada.metricas.filtro_especificacao.join(', ')
                      : 'Todos os tipos' }}
                </p>
              </div>
            </div>
          </Card>

          <Card class="bg-slate-800 border-slate-700 py-4 px-5">
            <div class="flex items-center gap-4">
              <div class="p-3 bg-slate-900 rounded-lg text-purple-500">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-slate-400">Eventos Exibidos</p>
                <p class="text-xl font-bold text-white">{{ jornada?.metricas?.numero_eventos_exibidos ?? '—' }}</p>
              </div>
            </div>
          </Card>

        </div>

        <!-- Desfecho e risco de readmissão -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card class="col-span-1 bg-slate-800 border-slate-700 py-4 px-5">
            <div class="flex items-center gap-2 mb-2">
              <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
              <p class="text-sm font-medium text-slate-300">Desfecho</p>
            </div>
            <span class="inline-block bg-purple-600 text-white text-xs px-3 py-1.5 rounded-md font-medium">
              Em Tratamento
            </span>
          </Card>

          <Card class="col-span-2 bg-red-900/20 border border-red-900/50 py-4 px-5">
            <div class="flex items-start gap-3">
              <svg class="w-5 h-5 text-red-500 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <div>
                <p class="text-sm font-medium text-red-400 mb-1">Risco de Readmissão</p>
                <p class="text-xs text-red-500/80">Paciente com múltiplas internações registradas</p>
              </div>
            </div>
          </Card>
        </div>

        <!-- Abas de navegação -->
        <div class="flex bg-slate-800 rounded-lg p-1 mt-2">
          <button
            @click="abaAtiva = 'linha-do-tempo'"
            :class="abaAtiva === 'linha-do-tempo' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white hover:bg-slate-700/50'"
            class="flex-1 flex items-center justify-center gap-2 py-3 px-4 rounded-md font-medium transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
            Linha do Tempo
          </button>
          <button
            @click="abaAtiva = 'analises'"
            :class="abaAtiva === 'analises' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white hover:bg-slate-700/50'"
            class="flex-1 flex items-center justify-center gap-2 py-3 px-4 rounded-md font-medium transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            Análises e Histórico
          </button>
        </div>

      </div>

      <!-- ANDAR INFERIOR: Linha do Tempo e Detalhes -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">

        <!-- COLUNA ESQUERDA -->
        <div class="lg:col-span-5 bg-slate-800 rounded-lg border border-slate-700 p-4 h-[600px] overflow-y-auto">

          <!-- ABA: Linha do Tempo -->
          <template v-if="abaAtiva === 'linha-do-tempo'">
            <h2 class="text-lg font-semibold text-white mb-4 sticky top-0 bg-slate-800 z-10 py-2">Linha do Tempo</h2>

            <!-- Eventos da jornada -->
            <div v-if="jornada?.eventos?.length" class="space-y-4">
              <div
                v-for="(item, index) in jornada.eventos"
                :key="`${item.tipo}-${index}`"
                class="relative group cursor-pointer"
                @click="selecionarEvento(item)"
              >
                <!-- Linha conectora -->
                <div
                  v-if="index !== jornada.eventos.length - 1"
                  class="absolute left-4 top-10 bottom-4 w-px bg-slate-600"
                ></div>

                <!-- Marcador da linha do tempo -->
                <div :class="[
                  'absolute left-2.5 top-5 w-3 h-3 rounded-full border-2 border-slate-800 z-10 transition-colors',
                  eventoSelecionado === item ? 'bg-purple-500' : corMarcadorPorTipo(item.tipo) + ' group-hover:bg-purple-400'
                ]"></div>

                <!-- Card do evento -->
                <div :class="[
                  'ml-10 border p-4 rounded-lg transition-all duration-200',
                  eventoSelecionado === item
                    ? 'bg-slate-700 border-purple-500 shadow-md'
                    : 'bg-slate-800/50 border-slate-700 hover:border-slate-500 hover:bg-slate-700/50'
                ]">
                  <div class="flex justify-between items-start mb-3">
                    <h3 class="font-semibold text-slate-100">{{ labelEvento(item) }}</h3>
                    <span class="text-[10px] font-bold px-2 py-1 rounded bg-slate-900 text-slate-300 uppercase border border-slate-700 tracking-wider">
                      {{ item.tipo }}
                    </span>
                  </div>

                  <div class="grid grid-cols-2 gap-2 text-xs text-slate-400 mt-2">
                    <div class="flex items-center gap-1.5">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      {{ formatarData(item.data_evento || item.dthr_inicio) }}
                    </div>

                    <div class="flex items-center gap-1.5">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.243-4.243a8 8 0 1111.314 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                      {{ item.unidade_executora || 'Hospital das Clínicas' }}
                    </div>

                    <div class="flex items-center gap-1.5">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      Duração: {{ item.tempo_permanencia_dias
                        ? item.tempo_permanencia_dias + ' dias'
                        : (item.duracao || 'Não informada') }}
                    </div>

                    <div class="flex items-center gap-1.5">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      {{ item.profissional || 'Equipe Médica' }}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-else class="text-sm text-slate-400 p-4 text-center">
              Nenhum evento encontrado para este paciente.
            </div>
          </template>

          <!-- ABA: Análises -->
          <template v-if="abaAtiva === 'analises'">
            <div class="space-y-4 animate-fade-in">

              <!-- Distribuição de tipos de evento -->
              <div class="bg-slate-800/80 rounded-lg border border-slate-700 p-5">
                <h3 class="text-white font-medium mb-4">Distribuição de Eventos</h3>
                <div class="space-y-3">
                  <div v-for="(qtd, tipo) in contagemPorTipo" :key="tipo" class="flex items-center gap-3">
                    <span class="text-xs text-slate-400 w-20 capitalize">{{ tipo }}</span>
                    <div class="flex-1 bg-slate-700 rounded-full h-2">
                      <div
                        class="h-2 rounded-full transition-all duration-500"
                        :class="corBarraPorTipo(tipo)"
                        :style="{ width: percentualTipo(qtd) + '%' }"
                      ></div>
                    </div>
                    <span class="text-xs font-bold text-white w-6 text-right">{{ qtd }}</span>
                  </div>
                  <p v-if="!Object.keys(contagemPorTipo).length" class="text-sm text-slate-400 text-center py-4">
                    Nenhum evento para exibir.
                  </p>
                </div>
              </div>

              <!-- Fatores de Risco -->
              <div class="bg-slate-800/80 rounded-lg border border-slate-700 p-5">
                <div class="flex items-center gap-2 mb-4">
                  <svg class="w-5 h-5 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                  <h3 class="text-white font-medium">Fatores de Risco</h3>
                </div>
                <div class="flex flex-wrap gap-2">
                  <span class="px-3 py-1 bg-orange-900/30 text-orange-400 border border-orange-900/50 rounded-full text-sm">Hipertensão</span>
                  <span class="px-3 py-1 bg-orange-900/30 text-orange-400 border border-orange-900/50 rounded-full text-sm">Diabetes tipo 2</span>
                  <span class="px-3 py-1 bg-orange-900/30 text-orange-400 border border-orange-900/50 rounded-full text-sm">Obesidade</span>
                </div>
              </div>

              <!-- Medicamentos em Uso -->
              <div class="bg-slate-800/80 rounded-lg border border-slate-700 p-5">
                <div class="flex items-center gap-2 mb-4">
                  <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                  </svg>
                  <h3 class="text-white font-medium">Medicamentos em Uso</h3>
                </div>
                <ul class="space-y-2 text-sm text-slate-300">
                  <li class="flex items-center gap-2"><div class="w-1.5 h-1.5 rounded-full bg-blue-500"></div> Furosemida 40mg</li>
                  <li class="flex items-center gap-2"><div class="w-1.5 h-1.5 rounded-full bg-blue-500"></div> Carvedilol 25mg</li>
                  <li class="flex items-center gap-2"><div class="w-1.5 h-1.5 rounded-full bg-blue-500"></div> Enalapril 20mg</li>
                  <li class="flex items-center gap-2"><div class="w-1.5 h-1.5 rounded-full bg-blue-500"></div> Espironolactona 25mg</li>
                  <li class="flex items-center gap-2"><div class="w-1.5 h-1.5 rounded-full bg-blue-500"></div> AAS 100mg</li>
                </ul>
              </div>

            </div>
          </template>
        </div>

        <!-- COLUNA DIREITA: Detalhes do Evento -->
        <div class="lg:col-span-7 bg-slate-800 rounded-lg border border-slate-700 p-6 h-[600px] overflow-y-auto relative">

          <!-- Estado vazio -->
          <div v-if="!eventoSelecionado" class="flex flex-col items-center justify-center h-full text-slate-400">
            <svg class="w-16 h-16 mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
            <p class="text-lg">Clique em um evento na linha do tempo</p>
            <p class="text-sm">para ver os detalhes completos aqui.</p>
          </div>

          <!-- Painel de detalhes do evento selecionado -->
          <div v-else class="animate-fade-in bg-slate-800/80 rounded-xl border border-slate-700 p-6 shadow-lg relative max-w-2xl mx-auto mt-4">

            <button @click="eventoSelecionado = null" class="absolute top-4 right-4 text-slate-400 hover:text-white transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>

            <!-- Título do evento -->
            <div class="mb-6">
              <h2 class="text-xl font-bold text-white mb-2">{{ labelEvento(eventoSelecionado) }}</h2>
              <p class="text-sm text-slate-400 leading-relaxed">
                {{ eventoSelecionado.descricao_origem_evento || 'Paciente em acompanhamento clínico.' }}
              </p>
            </div>

            <!-- Informações gerais do evento -->
            <div class="grid grid-cols-2 gap-y-6 gap-x-8 mb-8">
              <div>
                <p class="text-xs text-slate-500 mb-1">Data e Hora</p>
                <p class="text-sm font-medium text-slate-200">
                  {{ formatarData(eventoSelecionado.data_evento || eventoSelecionado.dthr_inicio) }}
                </p>
              </div>
              <div>
                <p class="text-xs text-slate-500 mb-1">Duração</p>
                <p class="text-sm font-medium text-slate-200">
                  {{ eventoSelecionado.tempo_permanencia_dias
                      ? eventoSelecionado.tempo_permanencia_dias + ' dias'
                      : (eventoSelecionado.duracao || 'Não informada') }}
                </p>
              </div>
              <div>
                <p class="text-xs text-slate-500 mb-1">Local</p>
                <p class="text-sm font-medium text-slate-200">
                  {{ eventoSelecionado.unidade_executora || 'Não informado' }}
                </p>
              </div>
              <div>
                <p class="text-xs text-slate-500 mb-1">Responsável</p>
                <p class="text-sm font-medium text-slate-200">
                  {{ eventoSelecionado.profissional || 'Equipe Médica' }}
                </p>
              </div>
            </div>

            <div class="border-t border-slate-700/50 mb-6"></div>

            <!-- Detalhes específicos por tipo de evento -->
            <div>
              <h3 class="text-sm font-medium text-slate-300 mb-4">Detalhes do Evento</h3>
              <div class="space-y-4">

                <!-- CONSULTA -->
                <template v-if="eventoSelecionado.tipo === 'consulta'">
                  <div class="flex justify-between items-center text-sm">
                    <span class="text-slate-500">Especialidade:</span>
                    <span class="font-medium text-slate-200 text-right">
                      {{ eventoSelecionado.especialidade || 'Não informada' }}
                    </span>
                  </div>
                  <div class="flex justify-between items-center text-sm">
                    <span class="text-slate-500">Queixa principal:</span>
                    <span class="font-medium text-slate-200 text-right">
                      {{ eventoSelecionado.justificativa || 'Não informada' }}
                    </span>
                  </div>
                  <div class="flex justify-between items-center text-sm">
                    <span class="text-slate-500">CID:</span>
                    <span class="font-medium text-slate-200 text-right">
                      {{ eventoSelecionado.cid || 'Não informado' }}
                    </span>
                  </div>
                  <div class="flex justify-between items-center text-sm">
                    <span class="text-slate-500">Procedimento:</span>
                    <span class="font-medium text-slate-200 text-right">
                      {{ eventoSelecionado.procedimento || 'Não informado' }}
                    </span>
                  </div>
                </template>

                <!-- EXAME -->
                <template v-else-if="eventoSelecionado.tipo === 'exame'">
                  <div class="flex justify-between items-center text-sm">
                    <span class="text-slate-500">Nome do Exame:</span>
                    <span class="font-medium text-slate-200 text-right">
                      {{ eventoSelecionado.nome_exame || 'Não informado' }}
                    </span>
                  </div>
                  <div class="flex justify-between items-center text-sm">
                    <span class="text-slate-500">Tipo de Exame:</span>
                    <span class="font-medium text-slate-200 text-right">
                      {{ eventoSelecionado.tipo_exame || 'Não informado' }}
                    </span>
                  </div>
                  <div class="flex justify-between items-center text-sm">
                    <span class="text-slate-500">Situação:</span>
                    <span class="font-medium text-emerald-400 text-right">
                      {{ eventoSelecionado.situacao_exame || 'Não informada' }}
                    </span>
                  </div>
                  <div class="flex justify-between items-center text-sm">
                    <span class="text-slate-500">Nº Atendimento:</span>
                    <span class="font-medium text-slate-200 text-right">
                      {{ eventoSelecionado.atendimento_id || 'Não informado' }}
                    </span>
                  </div>
                </template>

                <!-- INTERNAÇÃO -->
                <template v-else-if="eventoSelecionado.tipo === 'internacao'">
                  <div class="flex justify-between items-center text-sm">
                    <span class="text-slate-500">Origem:</span>
                    <span class="font-medium text-slate-200 text-right">
                      {{ eventoSelecionado.descricao_origem_evento || 'Não informada' }}
                    </span>
                  </div>
                  <div class="flex justify-between items-start text-sm">
                    <span class="text-slate-500 shrink-0">Sumário de Alta:</span>
                    <span class="font-medium text-slate-200 text-right max-w-[60%]">
                      {{ eventoSelecionado.situacao_sumario_alta || 'Não disponível' }}
                    </span>
                  </div>
                  <div class="flex justify-between items-center text-sm">
                    <span class="text-slate-500">Tipo da Alta:</span>
                    <span class="font-medium text-slate-200 text-right">
                      {{ eventoSelecionado.descricao_tipo_alta_medica || 'Não informado' }}
                    </span>
                  </div>
                </template>

                <!-- Tipo desconhecido -->
                <template v-else>
                  <p class="text-sm text-slate-400">Sem detalhes disponíveis para este tipo de evento.</p>
                </template>

              </div>
            </div>

          </div>
        </div>

      </div>

      <div class="mt-8">
        <Button @click="goBack" class="bg-slate-700 hover:bg-slate-600 text-white border-0">
          Voltar para a lista
        </Button>
      </div>

    </template>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import api from '../services/api';
import Card from '../components/Card.vue';
import Button from '../components/Button.vue';

const route = useRoute();
const router = useRouter();
const toast = useToast();

const codigo = String(route.params.codigo || '');

const jornada = ref<any | null>(null);
const carregando = ref(false);

const abaAtiva = ref<'linha-do-tempo' | 'analises'>('linha-do-tempo');
const eventoSelecionado = ref<any | null>(null);

// CORREÇÃO: Usando number em vez de NodeJS.Timeout
const dicaAtual = ref('Carregando dados do paciente...');
const etapaAtual = ref(1);
let dicaInterval: number | null = null;

const dicas = [
  'Carregando dados do paciente...',
  'Buscando histórico de consultas...',
  'Recuperando exames realizados...',
  'Organizando informações clínicas...',
  'Preparando linha do tempo...',
  'Quase pronto!'
];

// Computed para contagem de eventos
const contagemPorTipo = computed<Record<string, number>>(() => {
  if (!jornada.value?.eventos?.length) return {};
  return jornada.value.eventos.reduce((acc: Record<string, number>, ev: any) => {
    const tipo = ev.tipo || 'desconhecido';
    acc[tipo] = (acc[tipo] || 0) + 1;
    return acc;
  }, {});
});

const totalEventos = computed(() => jornada.value?.metricas?.numero_eventos || 1);

const percentualTipo = (qtd: number) =>
  Math.round((qtd / totalEventos.value) * 100);

// Funções auxiliares
const labelEvento = (item: any): string => {
  if (!item) return '';
  switch (item.tipo) {
    case 'consulta':
      return item.especialidade ? `Consulta — ${item.especialidade}` : 'Consulta Médica';
    case 'exame':
      return item.nome_exame || 'Exame';
    case 'internacao':
      return item.especialidade ? `Internação — ${item.especialidade}` : 'Internação';
    default:
      return item.tipo ?? 'Evento';
  }
};

const corMarcadorPorTipo = (tipo: string): string => {
  const cores: Record<string, string> = {
    consulta: 'bg-emerald-500',
    exame: 'bg-yellow-500',
    internacao: 'bg-orange-500',
  };
  return cores[tipo] ?? 'bg-slate-500';
};

const corBarraPorTipo = (tipo: string): string => {
  const cores: Record<string, string> = {
    consulta: 'bg-emerald-500',
    exame: 'bg-yellow-500',
    internacao: 'bg-orange-500',
  };
  return cores[tipo] ?? 'bg-slate-500';
};

const formatarData = (dataStr: string): string => {
  if (!dataStr) return 'Data não informada';
  try {
    const data = new Date(dataStr);
    if (isNaN(data.getTime())) return dataStr;
    const pad = (n: number) => String(n).padStart(2, '0');
    return `${pad(data.getDate())}/${pad(data.getMonth() + 1)}/${data.getFullYear()} às ${pad(data.getHours())}:${pad(data.getMinutes())}`;
  } catch {
    return dataStr;
  }
};

const selecionarEvento = (evento: any) => {
  eventoSelecionado.value = evento;
};

// Função para simular progresso durante o carregamento
const iniciarAnimacaoCarregamento = () => {
  let index = 0;
  dicaAtual.value = dicas[0];
  
  // CORREÇÃO: Usando window.setInterval e tipando como number
  dicaInterval = window.setInterval(() => {
    index = (index + 1) % dicas.length;
    dicaAtual.value = dicas[index];
    
    // Atualiza etapa para indicadores visuais
    if (index < 4) {
      etapaAtual.value = index + 1;
    }
  }, 1800);
};

// Função para carregar dados da jornada
const loadJornada = async () => {
  if (!codigo) {
    toast.error('Código de paciente inválido.');
    return;
  }

  carregando.value = true;
  iniciarAnimacaoCarregamento();

  try {
    const { data } = await api.get('/api/paciente/jornada', {
      params: { codigo },
    });

    jornada.value = data;

    if (data.eventos?.length) {
      eventoSelecionado.value = data.eventos[0];
    }

    // Completa o progresso
    etapaAtual.value = 4;
    dicaAtual.value = 'Carregamento concluído!';
    
    // Pequeno delay para mostrar o estado final
    await new Promise(resolve => setTimeout(resolve, 500));
    
  } catch (error) {
    toast.error('Não foi possível carregar a jornada do paciente.');
  } finally {
    carregando.value = false;
    if (dicaInterval !== null) {
      clearInterval(dicaInterval);
      dicaInterval = null;
    }
  }
};

const goBack = () => {
  router.push({ name: 'Pacientes' });
};

// Cleanup
onBeforeUnmount(() => {
  if (dicaInterval !== null) {
    clearInterval(dicaInterval);
    dicaInterval = null;
  }
});

onMounted(loadJornada);
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Animações de carregamento */
.animate-spin-slow {
  animation: spin 3s linear infinite;
}

.animate-spin-reverse {
  animation: spin 2s linear infinite reverse;
}

.animate-progress {
  animation: progress 2s ease-in-out infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes progress {
  0% { transform: translateX(-100%); }
  50% { transform: translateX(100%); }
  100% { transform: translateX(-100%); }
}

/* Efeito de brilho no anel de carregamento */
.animate-pulse {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.05); }
}
</style>