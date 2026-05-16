export interface Bike {
  id: number;
  slug: string;
  brand: string;
  model: string;
  build: string;
  country: string | null;
  status: string;
  motor: string | null;
  peak_w: number | null;
  peak_nm: number | null;
  battery_wh: number | null;
  battery_type: string | null;
  removable: string;
  front_travel_mm: number | null;
  rear_travel_mm: number | null;
  frame: string | null;
  wheels: string | null;
  weight_kg: number | null;
  weight_source: string | null;
  fork: string | null;
  shock: string | null;
  drivetrain: string | null;
  brakes: string | null;
  wheelset: string | null;
  dropper: string | null;
  instagram: string | null;
  notes: string | null;
  source_url: string | null;
  created_at: string;
  updated_at: string;
}

export interface Price {
  id: number;
  bike_id: number;
  currency: string;
  amount: number;
  source_url: string | null;
  verified_at: string | null;
}

export interface BikeImage {
  id: number;
  bike_id: number;
  url: string;
  sort_order: number;
  is_primary: number;
  alt_text: string | null;
}

export interface BikeWithRelations extends Bike {
  prices: Price[];
  images: BikeImage[];
}

export interface BikeListItem {
  id: number;
  slug: string;
  brand: string;
  model: string;
  build: string;
  country: string | null;
  status: string;
  motor: string | null;
  peak_w: number | null;
  peak_nm: number | null;
  battery_wh: number | null;
  removable: string;
  front_travel_mm: number | null;
  rear_travel_mm: number | null;
  frame: string | null;
  weight_kg: number | null;
  primary_image: string | null;
  prices: Record<string, number>;
}

export interface BikeOption {
  slug: string;
  brand: string;
  model: string;
  build: string;
}
