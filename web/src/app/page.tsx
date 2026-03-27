"use client";

import { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Search, MapPin, Clock, ExternalLink } from "lucide-react";

interface Course {
  id: string;
  name: string;
  institution_name: string;
  price_pen: number;
  mode: string;
  address: string;
  duration: string;
  url: string;
  distance_km?: number;
}

export default function Home() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);

  const fetchCourses = async (search = "") => {
    setLoading(true);
    try {
      const url = search 
        ? `http://localhost:8000/courses?name=${encodeURIComponent(search)}`
        : "http://localhost:8000/courses";
      const response = await fetch(url);
      const data = await response.json();
      setCourses(data);
    } catch (error) {
      console.error("Error fetching courses:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCourses();
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchCourses(searchTerm);
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-zinc-950 font-sans">
      {/* Header / Search Section */}
      <header className="bg-white dark:bg-zinc-900 border-b border-slate-200 dark:border-zinc-800 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 bg-indigo-600 rounded-lg flex items-center justify-center text-white font-bold text-xl">A</div>
              <h1 className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">Amauta.ai</h1>
            </div>
            
            <form onSubmit={handleSearch} className="flex-1 max-w-2xl flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                <Input 
                  type="text" 
                  placeholder="¿Qué quieres estudiar? (ej. Data Science, Marketing...)" 
                  className="pl-10 h-12 bg-slate-50 dark:bg-zinc-800 border-slate-200 dark:border-zinc-700 focus:ring-2 focus:ring-indigo-500"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
              <Button type="submit" className="h-12 px-6 bg-indigo-600 hover:bg-indigo-700 text-white transition-all">
                Buscar
              </Button>
            </form>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-xl font-semibold text-slate-900 dark:text-white">
            {loading ? "Buscando programas..." : `${courses.length} Programas encontrados`}
          </h2>
          <div className="flex gap-2">
            <Badge variant="outline" className="px-3 py-1">Lima, PE</Badge>
            <Badge variant="secondary" className="px-3 py-1">Ordenado por cercanía</Badge>
          </div>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[...Array(8)].map((_, i) => (
              <div key={i} className="h-[350px] bg-slate-200 dark:bg-zinc-800 animate-pulse rounded-xl" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {courses.map((course) => (
              <Card key={course.id} className="overflow-hidden border-slate-200 dark:border-zinc-800 hover:shadow-lg transition-all flex flex-col">
                <CardHeader className="pb-4">
                  <div className="flex justify-between items-start mb-2">
                    <Badge variant="outline" className="bg-slate-50 dark:bg-zinc-800">{course.institution_name}</Badge>
                    <Badge className="bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-100 border-0">
                      {course.mode}
                    </Badge>
                  </div>
                  <CardTitle className="text-lg leading-tight line-clamp-2 min-h-[3.5rem]">{course.name}</CardTitle>
                </CardHeader>
                <CardContent className="flex-1 space-y-4">
                  <div className="flex items-start gap-2 text-sm text-slate-600 dark:text-zinc-400">
                    <MapPin className="h-4 w-4 mt-0.5 shrink-0" />
                    <span className="line-clamp-2">{course.address}</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm text-slate-600 dark:text-zinc-400">
                    <Clock className="h-4 w-4" />
                    <span>{course.duration || "N/A"}</span>
                  </div>
                  {course.distance_km !== undefined && course.distance_km !== null && (
                    <div className="bg-indigo-50 dark:bg-indigo-950/30 text-indigo-700 dark:text-indigo-300 px-2 py-1 rounded text-xs font-medium inline-block">
                      A {course.distance_km.toFixed(1)} km de tu ubicación
                    </div>
                  )}
                </CardContent>
                <CardFooter className="pt-4 border-t border-slate-100 dark:border-zinc-800 bg-slate-50/50 dark:bg-zinc-900/50">
                  <div className="w-full flex justify-between items-center">
                    <div className="text-lg font-bold text-slate-900 dark:text-white">
                      {course.price_pen > 0 ? `S/ ${course.price_pen.toLocaleString()}` : "Gratis"}
                    </div>
                    <Button variant="ghost" size="sm" className="gap-1 text-indigo-600 hover:text-indigo-700 hover:bg-indigo-50" asChild>
                      <a href={course.url} target="_blank" rel="noopener noreferrer">
                        Ver más <ExternalLink className="h-3 w-3" />
                      </a>
                    </Button>
                  </div>
                </CardFooter>
              </Card>
            ))}
          </div>
        )}

        {!loading && courses.length === 0 && (
          <div className="text-center py-20 bg-white dark:bg-zinc-900 rounded-2xl border border-dashed border-slate-200 dark:border-zinc-800">
            <h3 className="text-lg font-medium mb-2">No encontramos resultados</h3>
            <p className="text-slate-500">Prueba con otros términos de búsqueda.</p>
          </div>
        )}
      </main>
    </div>
  );
}
