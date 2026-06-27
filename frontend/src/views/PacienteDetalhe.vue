<template>
  <div class="min-h-screen bg-slate-900 text-slate-200 p-6">
    <!-- ==========================================
         ANDAR SUPERIOR: Cabeçalho e Métricas
         ========================================== -->
    <div class="mb-8 space-y-4">
      
      <Card class="bg-slate-800 border-slate-700 p-6 relative">
        <button class="absolute top-6 right-6 text-yellow-500 hover:text-yellow-400">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
        </button>

        <h1 class="text-2xl font-bold text-white mb-1">Plataforma de Jornada Assistencial</h1>
        <p class="text-sm text-slate-400 mb-6">Hospital das Clínicas - Perspectiva do Paciente</p>
        
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center text-white text-lg font-bold">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
            </div>
            <div>
              <div class="text-slate-400 text-xs">Paciente</div>
              <div class="font-medium text-white">{{ jornada?.paciente?.nome ?? 'Carregando...' }}</div>
            </div>
          </div>
          <div>
            <div class="text-slate-400 text-xs">Prontuário</div>
            <div class="font-medium text-white">{{ jornada?.paciente?.prontuario ?? 'Carregando...' }}</div>
          </div>
          <div>
            <div class="text-slate-400 text-xs">Diagnóstico</div>
            <div class="font-medium text-white">Insuficiência Cardíaca Congestiva</div> </div>
          <div>
            <div class="text-slate-400 text-xs">CID</div>
            <div class="font-medium text-white">I50.0</div> </div>
        </div>
      </Card>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        
        <Card class="bg-slate-800 border-slate-700 py-4 px-5">
          <div class="flex items-center gap-4">
            <div class="p-3 bg-slate-900 rounded-lg text-blue-500">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            </div>
            <div>
              <p class="text-xs text-slate-400">Tempo Total de Atendimento</p>
              <p class="text-xl font-bold text-white">928h 32min</p>
            </div>
          </div>
        </Card>

        <Card class="bg-slate-800 border-slate-700 py-4 px-5">
          <div class="flex items-center gap-4">
            <div class="p-3 bg-slate-900 rounded-lg text-orange-500">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
            </div>
            <div>
              <p class="text-xs text-slate-400">Tempo Médio de Espera</p>
              <p class="text-xl font-bold text-white">330 min</p>
            </div>
          </div>
        </Card>

        <Card class="bg-slate-800 border-slate-700 py-4 px-5">
          <div class="flex items-center gap-4">
            <div class="p-3 bg-slate-900 rounded-lg text-purple-500">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            </div>
            <div>
              <p class="text-xs text-slate-400">Total de Eventos</p>
              <p class="text-xl font-bold text-white">{{ jornada?.metricas?.numero_eventos || 10 }}</p>
            </div>
          </div>
        </Card>

        <Card class="bg-slate-800 border-slate-700 py-4 px-5">
          <div class="flex items-center gap-4">
            <div class="p-3 bg-slate-900 rounded-lg text-yellow-500">
               <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
            </div>
            <div>
              <p class="text-xs text-slate-400">Exames Realizados</p>
              <p class="text-xl font-bold text-white">{{ jornada?.metricas?.numero_exames || 4 }}</p>
            </div>
          </div>
        </Card>

        <Card class="bg-slate-800 border-slate-700 py-4 px-5">
          <div class="flex items-center gap-4">
            <div class="p-3 bg-slate-900 rounded-lg text-emerald-500">
               <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            </div>
            <div>
              <p class="text-xs text-slate-400">Procedimentos</p>
              <p class="text-xl font-bold text-white">1</p> </div>
          </div>
        </Card>

        <Card class="bg-slate-800 border-slate-700 py-4 px-5">
          <div class="flex items-center gap-4">
            <div class="p-3 bg-slate-900 rounded-lg text-indigo-400">
               <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
            </div>
            <div>
              <p class="text-xs text-slate-400">Dias de Internação</p>
              <p class="text-xl font-bold text-white">{{ jornada?.metricas?.numero_internacoes || 38 }}</p> </div>
          </div>
        </Card>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card class="col-span-1 bg-slate-800 border-slate-700 py-4 px-5">
          <div class="flex items-center gap-2 mb-2">
            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
            <p class="text-sm font-medium text-slate-300">Desfecho</p>
          </div>
          <span class="inline-block bg-purple-600 text-white text-xs px-3 py-1.5 rounded-md font-medium">
            Em Tratamento
          </span>
        </Card>

        <Card class="col-span-2 bg-red-900/20 border border-red-900/50 py-4 px-5">
          <div class="flex items-start gap-3">
            <svg class="w-5 h-5 text-red-500 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
            <div>
              <p class="text-sm font-medium text-red-400 mb-1">Risco de Readmissão</p>
              <p class="text-xs text-red-500/80">Paciente com 2 internações anteriores (últimos 6 meses)</p>
            </div>
          </div>
        </Card>
      </div>

      <!-- para os botões-->
      <div class="flex bg-slate-800 rounded-lg p-1 mt-2">
        <button 
          @click="abaAtiva = 'linha-do-tempo'"
          :class="abaAtiva === 'linha-do-tempo' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white hover:bg-slate-700/50'"
          class="flex-1 flex items-center justify-center gap-2 py-3 px-4 rounded-md font-medium transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
          Linha do Tempo
        </button>
        <button 
          @click="abaAtiva = 'analises'"
          :class="abaAtiva === 'analises' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white hover:bg-slate-700/50'"
          class="flex-1 flex items-center justify-center gap-2 py-3 px-4 rounded-md font-medium transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
          Análises e Histórico
        </button>
      </div>

    </div>

    <!-- ==========================================
         ANDAR INFERIOR: Grid com Linha do Tempo e Detalhes
         ========================================== -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
      
      <!-- COLUNA ESQUERDA (Linha do Tempo) -->
      
      <div class="lg:col-span-5 bg-slate-800 rounded-lg border border-slate-700 p-4 h-[600px] overflow-y-auto">
        
        <template v-if="abaAtiva === 'linha-do-tempo'">
          <h2 class="text-lg font-semibold text-white mb-4 sticky top-0 bg-slate-800 z-10 py-2">Linha do Tempo</h2>
          
          <div v-if="jornada?.eventos?.length" class="space-y-4">
            <div v-for="(item, index) in jornada.eventos" :key="`${item.tipo}-${index}`" class="relative group cursor-pointer" @click="selecionarEvento(item)">
              
              <div v-if="index !== jornada.eventos.length - 1" class="absolute left-4 top-10 bottom-[-1rem] w-px bg-slate-600"></div>

              <div :class="[
                'absolute left-2.5 top-5 w-3 h-3 rounded-full border-2 border-slate-800 z-10 transition-colors',
                eventoSelecionado === item ? 'bg-purple-500' : 'bg-slate-500 group-hover:bg-purple-400'
              ]"></div>

              <div :class="[
                'ml-10 border p-4 rounded-lg transition-all duration-200',
                eventoSelecionado === item 
                  ? 'bg-slate-700 border-purple-500 shadow-md' 
                  : 'bg-slate-800/50 border-slate-700 hover:border-slate-500 hover:bg-slate-700/50'
              ]">
                <div class="flex justify-between items-start mb-3">
                  <h3 class="font-semibold text-slate-100">
                    <span v-if="item.tipo === 'consulta'">Consulta Médica</span>
                    <span v-else-if="item.tipo === 'exame'">{{ item.nome_exame || 'Exame' }}</span>
                    <span v-else-if="item.tipo === 'internacao'">Internação</span>
                  </h3>
                  <span class="text-[10px] font-bold px-2 py-1 rounded bg-slate-900 text-slate-300 uppercase border border-slate-700 tracking-wider">
                    {{ item.tipo }}
                  </span>
                </div>
                
                <div class="grid grid-cols-2 gap-2 text-xs text-slate-400 mt-2">
                  
                  <div class="flex items-center gap-1.5">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    {{ formatarData(item.data_evento || item.dthr_inicio) }}
                  </div>

                  <div class="flex items-center gap-1.5">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.243-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                    {{ item.unidade_executora || 'Hospital das Clínicas' }}
                  </div>

                  <div class="flex items-center gap-1.5">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    Duração: {{ item.tempo_permanencia_dias ? item.tempo_permanencia_dias + ' dias' : (item.duracao || '45 min') }}
                  </div>

                  <div class="flex items-center gap-1.5">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
                    {{ item.profissional || 'Equipe Médica' }}
                  </div>

                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-sm text-slate-400 p-4 text-center">Nenhum evento encontrado.</div>
        </template>

        <template v-if="abaAtiva === 'analises'">
          <div class="space-y-4 animate-fade-in">
            
            <div class="bg-slate-800/80 rounded-lg border border-slate-700 p-5">
              <h3 class="text-white font-medium mb-6">Distribuição de Eventos na Jornada Atual</h3>
              
              <div class="relative flex justify-center items-center h-48 mt-8 mb-4">
                <div class="w-40 h-40 rounded-full border-2 border-slate-800 shadow-md"
                     style="background: conic-gradient(
                       #10b981 0% 20%,     
                       #a855f7 20% 30%,    
                       #3b82f6 30% 40%,    
                       #ef4444 40% 50%,    
                       #f97316 50% 60%,    
                       #eab308 60% 100%    
                     );">
                </div>
                
                <span class="absolute top-[-10px] left-10 text-emerald-500 text-sm font-medium">Consulta: 2</span>
                <span class="absolute top-2 right-12 text-purple-400 text-sm font-medium">Triagem: 1</span>
                <span class="absolute top-1/4 right-6 text-blue-500 text-sm font-medium">Entrada: 1</span>
                <span class="absolute top-1/2 right-0 text-red-500 text-sm font-medium">Procedimento: 1</span>
                <span class="absolute bottom-6 right-6 text-orange-500 text-sm font-medium">Internacao: 1</span>
                <span class="absolute bottom-2 left-10 text-yellow-500 text-sm font-medium">Exame: 4</span>
              </div>
            </div>

            <div class="bg-slate-800/80 rounded-lg border border-slate-700 p-5">
              <div class="flex items-center gap-2 mb-4">
                <svg class="w-5 h-5 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                <h3 class="text-white font-medium">Fatores de Risco</h3>
              </div>
              <div class="flex flex-wrap gap-2">
                <span class="px-3 py-1 bg-orange-900/30 text-orange-400 border border-orange-900/50 rounded-full text-sm">Hipertensão</span>
                <span class="px-3 py-1 bg-orange-900/30 text-orange-400 border border-orange-900/50 rounded-full text-sm">Diabetes tipo 2</span>
                <span class="px-3 py-1 bg-orange-900/30 text-orange-400 border border-orange-900/50 rounded-full text-sm">Obesidade</span>
              </div>
            </div>

            <div class="bg-slate-800/80 rounded-lg border border-slate-700 p-5">
              <div class="flex items-center gap-2 mb-4">
                <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path></svg>
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

      <!-- COLUNA DIREITA (Detalhes do Evento) -->
      
      <div class="lg:col-span-7 bg-slate-800 rounded-lg border border-slate-700 p-6 h-[600px] overflow-y-auto relative">
        
        <div v-if="!eventoSelecionado" class="flex flex-col items-center justify-center h-full text-slate-400">
          <svg class="w-16 h-16 mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
          <p class="text-lg">Clique em um evento na linha do tempo</p>
          <p class="text-sm">para ver os detalhes completos aqui.</p>
        </div>

        <div v-else class="animate-fade-in bg-slate-800/80 rounded-xl border border-slate-700 p-6 shadow-lg relative max-w-2xl mx-auto mt-4">
          
          <button @click="eventoSelecionado = null" class="absolute top-4 right-4 text-slate-400 hover:text-white transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>

          <div class="mb-6">
            <h2 class="text-xl font-bold text-white mb-2">
              <span v-if="eventoSelecionado.tipo === 'consulta'">Consulta - {{ eventoSelecionado.especialidade || 'Cardiologia' }}</span>
              <span v-else-if="eventoSelecionado.tipo === 'exame'">{{ eventoSelecionado.nome_exame || 'Exame' }}</span>
              <span v-else-if="eventoSelecionado.tipo === 'internacao'">Internação - {{ eventoSelecionado.especialidade || 'Geral' }}</span>
            </h2>
            <p class="text-sm text-slate-400 leading-relaxed">
               {{ eventoSelecionado.descricao_origem_evento || 'Paciente deu entrada para avaliação clínica e acompanhamento de rotina.' }}
            </p>
          </div>

          <div class="grid grid-cols-2 gap-y-6 gap-x-8 mb-8">
            <div>
              <p class="text-xs text-slate-500 mb-1">Data e Hora</p>
              <p class="text-sm font-medium text-slate-200">{{ formatarData(eventoSelecionado.data_evento || eventoSelecionado.dthr_inicio) }}</p>
            </div>
            <div>
              <p class="text-xs text-slate-500 mb-1">Duração</p>
              <p class="text-sm font-medium text-slate-200">{{ eventoSelecionado.tempo_permanencia_dias ? eventoSelecionado.tempo_permanencia_dias + ' dias' : (eventoSelecionado.duracao || '45 minutos') }}</p>
            </div>
            <div>
              <p class="text-xs text-slate-500 mb-1">Local</p>
              <p class="text-sm font-medium text-slate-200">{{ eventoSelecionado.unidade_executora || 'PS - Recepção' }}</p>
            </div>
            <div>
              <p class="text-xs text-slate-500 mb-1">Responsável</p>
              <p class="text-sm font-medium text-slate-200">{{ eventoSelecionado.profissional || 'Dr. Carlos Mendes' }}</p>
            </div>
          </div>

          <div class="border-t border-slate-700/50 mb-6"></div>

          <div>
            <h3 class="text-sm font-medium text-slate-300 mb-4">Detalhes do Evento</h3>
            
            <div class="space-y-4">
              <template v-if="eventoSelecionado.tipo === 'consulta'">
                <div class="flex justify-between items-center text-sm">
                  <span class="text-slate-500">Queixa principal:</span>
                  <span class="font-medium text-slate-200 text-right">{{ eventoSelecionado.justificativa || 'Dispneia aos esforços' }}</span>
                </div>
                <div class="flex justify-between items-center text-sm">
                  <span class="text-slate-500">CID:</span>
                  <span class="font-medium text-slate-200 text-right">{{ eventoSelecionado.cid || 'Não informado' }}</span>
                </div>
                <div class="flex justify-between items-center text-sm">
                  <span class="text-slate-500">Procedimento:</span>
                  <span class="font-medium text-slate-200 text-right">{{ eventoSelecionado.procedimento || 'Avaliação padrão' }}</span>
                </div>
              </template>

              <template v-else-if="eventoSelecionado.tipo === 'exame'">
                <div class="flex justify-between items-center text-sm">
                  <span class="text-slate-500">Tipo de Exame:</span>
                  <span class="font-medium text-slate-200 text-right">{{ eventoSelecionado.tipo_exame || 'Laboratorial' }}</span>
                </div>
                <div class="flex justify-between items-center text-sm">
                  <span class="text-slate-500">Situação:</span>
                  <span class="font-medium text-emerald-400 text-right">{{ eventoSelecionado.situacao_exame || 'Concluído' }}</span>
                </div>
                <div class="flex justify-between items-center text-sm">
                  <span class="text-slate-500">Nº Atendimento:</span>
                  <span class="font-medium text-slate-200 text-right">{{ eventoSelecionado.atendimento_id || 'Não informado' }}</span>
                </div>
              </template>

              <template v-else-if="eventoSelecionado.tipo === 'internacao'">
                <div class="flex justify-between items-center text-sm">
                  <span class="text-slate-500">Origem:</span>
                  <span class="font-medium text-slate-200 text-right">{{ eventoSelecionado.descricao_origem_evento || 'Pronto Socorro' }}</span>
                </div>
                <div class="flex justify-between items-center text-sm">
                  <span class="text-slate-500">Sumário de Alta:</span>
                  <span class="font-medium text-slate-200 text-right max-w-[60%]">{{ eventoSelecionado.situacao_sumario_alta || 'Paciente estável, alta médica concedida.' }}</span>
                </div>
                <div class="flex justify-between items-center text-sm">
                  <span class="text-slate-500">Tipo da Alta:</span>
                  <span class="font-medium text-slate-200 text-right">{{ eventoSelecionado.descricao_tipo_alta_medica || 'Melhora' }}</span>
                </div>
              </template>
            </div>
          </div>

        </div>
      </div>

    </div>
    
    <div class="mt-8">
      <Button @click="goBack" class="bg-slate-700 hover:bg-slate-600 text-white border-0">Voltar para a lista</Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
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

// 
const abaAtiva = ref('linha-do-tempo'); // Pode ser 'linha-do-tempo' ou 'analises'

// NOSSO NOVO ESTADO: Guarda o evento que o usuário clicou
const eventoSelecionado = ref<any | null>(null);

const selecionarEvento = (evento: any) => {
  eventoSelecionado.value = evento;
};

const loadJornada = async () => {
  if (!codigo) {
    toast.error('Código de paciente inválido.');
    return;
  }

  try {
    const { data } = await api.get('/api/paciente/jornada', { params: { codigo } });
    jornada.value = data;
    
    // Opcional: Se quiser que o primeiro item já venha aberto ao carregar a tela
    if (data.eventos && data.eventos.length > 0) {
      eventoSelecionado.value = data.eventos[0];
    }
    
  } catch (error) {
    toast.error('Não foi possível carregar a jornada do paciente.');
  }
};

const goBack = () => {
  router.push({ name: 'Pacientes' });
};

// função para formatar data e hora 
const formatarData = (dataStr: string) => {
  if (!dataStr) return 'Data não informada';
  try {
    const data = new Date(dataStr);
    const dia = String(data.getDate()).padStart(2, '0');
    const mes = String(data.getMonth() + 1).padStart(2, '0');
    const ano = data.getFullYear();
    const horas = String(data.getHours()).padStart(2, '0');
    const minutos = String(data.getMinutes()).padStart(2, '0');
    
    return `${dia}/${mes}/${ano} às ${horas}:${minutos}`;
  } catch (e) {
    return dataStr;
  }
};

onMounted(loadJornada);
</script>

<style scoped>
/* Pequena animação para quando o conteúdo da direita trocar */
.animate-fade-in {
  animation: fadeIn 0.3s ease-in-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>