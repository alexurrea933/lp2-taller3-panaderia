'use client';

import useSWR from 'swr';
import { fetcher, type Producto } from '@/lib/api';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Spinner } from '@/components/ui/spinner';
import { Package } from 'lucide-react';

export function ProductosTable() {
  const { data: productos, error, isLoading } = useSWR<Producto[]>('/api/productos', fetcher);

  if (isLoading) {
    return (
      <Card>
        <CardContent className="flex items-center justify-center py-12">
          <Spinner className="size-8" />
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardContent className="py-12">
          <div className="text-center text-muted-foreground">
            <p>No se pudo conectar con la API.</p>
            <p className="text-sm mt-2">Asegúrate de que el backend esté corriendo en el puerto 8000.</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Package className="size-5" />
          Productos
        </CardTitle>
      </CardHeader>
      <CardContent>
        {productos && productos.length > 0 ? (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Nombre</TableHead>
                <TableHead>Precio</TableHead>
                <TableHead>Stock</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {productos.map((producto) => (
                <TableRow key={producto.id}>
                  <TableCell className="font-medium">{producto.id}</TableCell>
                  <TableCell>{producto.nombre}</TableCell>
                  <TableCell>${producto.precio.toFixed(2)}</TableCell>
                  <TableCell>
                    {producto.stock !== undefined ? (
                      <Badge variant={producto.stock > 10 ? 'default' : 'destructive'}>
                        {producto.stock}
                      </Badge>
                    ) : (
                      '-'
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        ) : (
          <p className="text-center text-muted-foreground py-8">No hay productos disponibles.</p>
        )}
      </CardContent>
    </Card>
  );
}
