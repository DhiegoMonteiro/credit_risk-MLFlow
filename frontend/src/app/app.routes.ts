import { Routes } from '@angular/router';
import { DataInputComponent } from './data-input/data-input.component';
import { ResultsComponent } from './results/results.component';

export const routes: Routes = [
  { path: '', redirectTo: 'input', pathMatch: 'full' },
  { path: 'input', component: DataInputComponent },
  { path: 'results', component: ResultsComponent },
  { path: '**', redirectTo: 'input' }
];
