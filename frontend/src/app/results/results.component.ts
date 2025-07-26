import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

interface FormData {
  person_age: number;
  person_income: number;
  person_home_ownership: number;
  person_emp_length: number;
  loan_intent: number;
  loan_grade: number;
  loan_amnt: number;
  loan_int_rate: number;
  loan_percent_income: number;
  cb_person_default_on_file: number;
  cb_person_cred_hist_length: number;
}

interface PredictionResult {
  prediction: number;
  status: string;
  confidence: number;
}

@Component({
  selector: 'app-results',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})

export class ResultsComponent implements OnInit {
  private router = inject(Router);

  formData: FormData | null = null;
  result: PredictionResult | null = null;

  homeOwnershipLabels = ['Aluguel', 'Própria', 'Hipoteca', 'Outro'];
  loanIntentLabels = ['Pessoal', 'Educação', 'Médico', 'Empreendimento', 'Melhoria da Casa', 'Consolidação de Dívidas'];
  loanGradeLabels = ['A', 'B', 'C', 'D', 'E', 'F', 'G'];
  defaultOnFileLabels = ['Não', 'Sim'];

  ngOnInit(): void {
    const { formData, result } = history.state as {
      formData?: FormData;
      result?: PredictionResult;
    };

    if (formData && result) {
      this.formData = formData;
      this.result = result;
    } else {
      this.router.navigate(['/input']);
    }
  }

  getLabelForHomeOwnership(value: number): string {
    return this.homeOwnershipLabels[value] || 'Unknown';
  }

  getLabelForLoanIntent(value: number): string {
    return this.loanIntentLabels[value] || 'Unknown';
  }

  getLabelForLoanGrade(value: number): string {
    return this.loanGradeLabels[value] || 'Unknown';
  }

  getLabelForDefaultOnFile(value: number): string {
    return this.defaultOnFileLabels[value] || 'Unknown';
  }

  getConfidencePercent(): string {
    return this.result ? (this.result.confidence * 100).toFixed(2) : '0%';
  }

  startNewAssessment(): void {
    this.router.navigate(['/input']);
  }
}