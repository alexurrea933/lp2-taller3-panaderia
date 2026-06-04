import { StatsCards } from '@/components/stats-cards';
import { ProductosTable } from '@/components/productos-table';
import { ClientesTable } from '@/components/clientes-table';

export default function Page() {
  return (
    <main className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <header className="mb-8">
          <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-muted-foreground mt-1">
            Panel de control conectado a tu API FastAPI
          </p>
        </header>

        <div className="space-y-8">
          <StatsCards />

          <div className="grid gap-6 lg:grid-cols-2">
            <ProductosTable />
            <ClientesTable />
          </div>
        </div>

        <footer className="mt-12 border-t pt-6 text-center text-sm text-muted-foreground">
          <p>
            API Backend: <code className="rounded bg-muted px-1.5 py-0.5">http://127.0.0.1:8000</code>
          </p>
        </footer>
      </div>
    </main>
  );
}
