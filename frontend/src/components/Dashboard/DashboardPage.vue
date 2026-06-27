<DashboardFilters
  @search="loadDashboard"
/>

<DashboardKpis
  :kpis="dashboard?.kpis"
/>

<JourneyTimeline
  :etapas="dashboard?.etapas"
/>