<template>
  <section class="flex flex-col gap-12">
    <div class="grid gap-6 lg:grid-cols-2 lg:items-center">
      <div class="space-y-6">
        <span class="inline-flex items-center rounded-full bg-ocean-100 px-4 py-1 text-sm font-semibold text-ocean-700">
          Intelligent maritime insights
        </span>
        <h1 class="text-4xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-5xl">
          Navigate the future of ocean analytics with confidence.
        </h1>
        <p class="text-lg text-slate-600 dark:text-slate-300">
          BlueSea combines real-time telemetry, predictive modeling, and collaborative planning tools to help your teams operate more sustainably on the water.
        </p>
        <div class="flex flex-wrap gap-4">
          <Button label="Request a demo" severity="primary" size="large" />
          <Button label="Learn more" severity="secondary" size="large" outlined />
        </div>
      </div>
      <div class="relative">
        <div class="aspect-square overflow-hidden rounded-3xl bg-gradient-to-br from-ocean-400 via-blue-500 to-slate-900 shadow-2xl">
          <div class="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(255,255,255,0.35),_rgba(255,255,255,0))]"></div>
          <div class="absolute inset-x-10 inset-y-16 rounded-2xl border border-white/20 bg-white/10 backdrop-blur">
            <div class="flex h-full items-center justify-center">
              <p class="text-center text-lg font-semibold text-white">
                Operational overview<br />
                <span class="text-sm font-normal text-slate-200">Live fleet performance metrics</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="grid gap-6 border-t border-slate-200 pt-8 dark:border-slate-700 md:grid-cols-3">
      <div class="space-y-3">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">Real-time monitoring</h2>
        <p class="text-slate-600 dark:text-slate-300">
          Streaming dashboards unify environmental conditions and vessel telematics so you can respond instantly to shifting seas.
        </p>
      </div>
      <div class="space-y-3">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">Predictive routing</h2>
        <p class="text-slate-600 dark:text-slate-300">
          AI-powered recommendations reduce fuel consumption and emissions across your fleet's most critical routes.
        </p>
      </div>
      <div class="space-y-3">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">Collaborative planning</h2>
        <p class="text-slate-600 dark:text-slate-300">
          Role-based workspaces let teams coordinate maintenance windows, compliance tasks, and voyage plans with clarity.
        </p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import Button from 'primevue/button';
</script>
