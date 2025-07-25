import { Routes } from '@angular/router';
import { DataInputComponent } from './data-input/data-input.component';
import { ResultsComponent } from './results/results.component';
import { CsvUploadComponent } from './csv-upload/csv-upload.component';

export const routes: Routes = [
  { path: '', redirectTo: 'input', pathMatch: 'full' },
  { path: 'input', component: DataInputComponent },
  { path: 'results', component: ResultsComponent },
  {path: 'csv-upload', component: CsvUploadComponent},
  { path: '**', redirectTo: 'input' }
];
