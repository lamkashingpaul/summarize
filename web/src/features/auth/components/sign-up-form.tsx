"use client";

import { signUpSchema } from "@/features/auth/schemas/sign-up.schema";
import { SubmitHandler, useForm } from "react-hook-form";
import { z } from "zod/v4";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { InputWithAnEye } from "@/components/ui/input-with-an-eye";
import Link from "next/link";
import { useSignUp } from "@/features/auth/api/use-sign-up";
import { Checkbox } from "@/components/ui/checkbox";
import { formatErrorMessage } from "@/lib/utils";
import { AlertSuccess } from "@/components/ui/alert-success";
import { AlertFailure } from "@/components/ui/alert-failure";
import { ButtonWithLoading } from "@/components/ui/button-with-loading";
import { useEffect } from "react";

type SignUpFormInput = z.input<typeof signUpSchema>;
type SignUpFormOutput = z.output<typeof signUpSchema>;

export const SignUpForm = () => {
  const {
    mutateAsync: signUp,
    data: signUpData,
    isPending: isSignUpPending,
  } = useSignUp();

  const form = useForm({
    defaultValues: getSignUpFormDefaultValues,
    resolver: zodResolver(signUpSchema),
    disabled: isSignUpPending,
  });

  const {
    handleSubmit,
    control,
    setError,
    reset,
    formState: { errors, isSubmitSuccessful },
  } = form;

  const onSubmit: SubmitHandler<SignUpFormOutput> = async (data) => {
    try {
      await signUp(data);
    } catch (error) {
      const errorMessage = formatErrorMessage(error);
      setError("root.serverError", { type: "server", message: errorMessage });
    }
  };

  useEffect(() => {
    if (isSubmitSuccessful) {
      reset({ ...getSignUpFormDefaultValues, agreedToTerms: true });
    }
  }, [isSubmitSuccessful, reset]);

  return (
    <Form {...form}>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {signUpData?.detail ? (
          <AlertSuccess
            title="Account Created"
            description={`${signUpData.detail} Please check your email for verification instructions.`}
          />
        ) : null}

        {errors?.root?.serverError?.type === "server" ? (
          <AlertFailure
            title="Sign Up Failed"
            description={errors.root.serverError.message}
          />
        ) : null}

        <FormField
          control={control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input placeholder="John Doe" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input placeholder="john.doe@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Password</FormLabel>
              <FormControl>
                <InputWithAnEye
                  placeholder="Create a strong password"
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={control}
          name="confirmPassword"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Confirm Password</FormLabel>
              <FormControl>
                <InputWithAnEye
                  placeholder="Confirm your password"
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={control}
          name="agreedToTerms"
          render={({ field }) => (
            <FormItem className="flex flex-col items-start space-x-2">
              <FormLabel className="hover:bg-accent/50 flex w-full items-start gap-3 rounded-lg border p-3 has-[[aria-checked=true]]:border-blue-600 has-[[aria-checked=true]]:bg-blue-50 dark:has-[[aria-checked=true]]:border-blue-900 dark:has-[[aria-checked=true]]:bg-blue-950">
                <FormControl>
                  <Checkbox
                    checked={field.value}
                    onCheckedChange={(checked) =>
                      field.onChange(checked as boolean)
                    }
                    className="data-[state=checked]:border-blue-600 data-[state=checked]:bg-blue-600 data-[state=checked]:text-white dark:data-[state=checked]:border-blue-700 dark:data-[state=checked]:bg-blue-700"
                  />
                </FormControl>
                <div className="text-xs">
                  I agree to the{" "}
                  <Link
                    href="/terms"
                    rel="noopener noreferrer"
                    target="_blank"
                    className="text-primary hover:underline"
                  >
                    Terms of Service
                  </Link>{" "}
                  and{" "}
                  <Link
                    href="/privacy"
                    rel="noopener noreferrer"
                    target="_blank"
                    className="text-primary hover:underline"
                  >
                    Privacy Policy
                  </Link>
                </div>
              </FormLabel>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={control}
          name="subscribeToNewsletter"
          render={({ field }) => (
            <FormItem className="flex flex-col items-start space-x-2">
              <FormLabel className="hover:bg-accent/50 flex w-full items-start gap-3 rounded-lg border p-3 has-[[aria-checked=true]]:border-blue-600 has-[[aria-checked=true]]:bg-blue-50 dark:has-[[aria-checked=true]]:border-blue-900 dark:has-[[aria-checked=true]]:bg-blue-950">
                <FormControl>
                  <Checkbox
                    checked={field.value}
                    onCheckedChange={(checked) =>
                      field.onChange(checked as boolean)
                    }
                    className="data-[state=checked]:border-blue-600 data-[state=checked]:bg-blue-600 data-[state=checked]:text-white dark:data-[state=checked]:border-blue-700 dark:data-[state=checked]:bg-blue-700"
                  />
                </FormControl>
                <div className="grid gap-1.5 font-normal">
                  <p className="text-xs leading-none font-medium">
                    Subscribe to our newsletter for research insights and
                    product updates
                  </p>
                  <p className="text-muted-foreground text-xs">
                    You can enable or disable notifications at any time.
                  </p>
                </div>
              </FormLabel>
              <FormMessage />
            </FormItem>
          )}
        />

        <ButtonWithLoading
          type="submit"
          className="w-full"
          isLoading={isSignUpPending}
        >
          Create Account
        </ButtonWithLoading>
      </form>
    </Form>
  );
};

const getSignUpFormDefaultValues = {
  name: "",
  email: "",
  password: "",
  confirmPassword: "",
  agreedToTerms: false,
  subscribeToNewsletter: true,
} satisfies SignUpFormInput;
