export interface Spoorkabel {
  id: number;
  kabelnummer: number | null;
  kabel_geboren: string | null;
  kabelnaam: string | null;
  kabelnaam_oud: string | null;
  van: string | null;
  naar: string | null;
  kabeltype: string | null;
  groep: string | null;
  sub_groep: string | null;
  van_gil: string | null;
  naar_gil: string | null;
  geulen: number[];
  geulen_not_found: number[] | null;
  opmerking: string | null;
  max_lengte: number | null;
  tb_lengte: number | null;
  ab_lengte: number | null;
  regelnummer: string | number | null;
  created_at: string;
  edited_at: string;
}

// Geometry types
export interface Point {
  type: 'Point';
  coordinates: [number, number];
}

export interface LineString {
  type: 'LineString';
  coordinates: [number, number][];
}

export interface MultiLineString {
  type: 'MultiLineString';
  coordinates: [number, number][][];
}

export interface Polygon {
  type: 'Polygon';
  coordinates: [number, number][][];
}

export type Geometry = Point | LineString | MultiLineString | Polygon;

// Feature types
export interface SpoorkabelFeature {
  type: 'Feature';
  geometry: Geometry;
  properties: Spoorkabel;
  id?: string | number;
}

export interface SpoorkabelFeatureCollection {
  type: 'FeatureCollection';
  features: SpoorkabelFeature[];
}

// Alias for convenience
export type SpoorkabelGeoJSON = SpoorkabelFeatureCollection;