'use client';

import useSWR from 'swr';
import { fetcher } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Package, Users, Activity } from 'lucide-react';

export function StatsCards() {
  const { data: productos } = useSWR('/api/productos', fetcher);
  const { data: clientes } = useSWR('/api/clientes', fetcher);

  const stats = [
    {
      title: 'Total Productos',
      value: productos?.length ?? 0,
      icon: Package,
      color: 'text-blue-500',
    },
    {
      title: 'Total Clientes',
      value: clientes?.length ?? 0,
      icon: Users,
      color: 'text-green-500',
    },
    {
      title: 'Estado API',
      value: productos || clientes ? 'Conectado' : 'Desconectado',
      icon: Activity,
      badge: true,
      connected: !!(productos || clientes),
    },
  ];

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {stats.map((stat) => (
        <Card key={stat.title}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
            <stat.icon className={`size-4 ${stat.color || 'text-muted-foreground'}`} />
          </CardHeader>
          <CardContent>
            {stat.badge ? (
              <Badge variant={stat.connected ? 'default' : 'destructive'}>
                {stat.value}
              </Badge>
            ) : (
              <div className="text-2xl font-bold">{stat.value}</div>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
