"use client";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { ResetPasswordForm } from "@/features/auth/components/reset-password-form";
import { ArrowLeft, FileText } from "lucide-react";
import Link from "next/link";
import { useQueryState } from "nuqs";
import { Suspense } from "react";

export default function SuspenseResetPasswordPage() {
  return (
    <Suspense>
      <ResetPasswordPage />
    </Suspense>
  );
}

function ResetPasswordPage() {
  const [token] = useQueryState("token", { defaultValue: "" });

  return (
    <section className="my-auto">
      <div className="container-wrapper !max-w-md">
        <div className="container">
          <div className="mb-8 text-center">
            <Link
              href="/"
              className="text-muted-foreground hover:text-foreground mb-6 inline-flex items-center gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              <span>Back to Summarize</span>
            </Link>
            <div className="mb-2 flex items-center justify-center gap-2">
              <FileText className="text-primary h-8 w-8" />
              <span className="text-2xl font-bold">Summarize</span>
            </div>
            <p className="text-muted-foreground">Create your new password</p>
          </div>
        </div>

        <Card>
          <CardHeader className="space-y-1">
            <CardTitle className="text-center text-2xl font-bold">
              Reset Password
            </CardTitle>
            <CardDescription className="text-center">
              Enter your new password below
            </CardDescription>
          </CardHeader>

          <CardContent className="space-y-4">
            <ResetPasswordForm token={token} />

            <div className="bg-muted/30 mt-6 rounded-lg p-4">
              <h4 className="mb-2 text-sm font-medium">Security Tips:</h4>
              <ul className="text-muted-foreground list-inside list-disc space-y-1 text-xs">
                <li>Use a unique password you haven&apos;t used elsewhere</li>
                <li>Consider using a password manager</li>
                <li>You&apos;ll be signed out of all devices for security</li>
              </ul>
            </div>
          </CardContent>
        </Card>
      </div>
    </section>
  );
}
