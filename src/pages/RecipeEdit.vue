<script setup lang="ts">
import type { EditableRecipe, Food, Qualifier, Unit } from "@/types/recipes";
import type { User } from "@/types/users";

import { Deferred, useForm } from "@inertiajs/vue3";
import { computed } from "vue";
import { useI18n } from "vue-i18n";

import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import DescriptionItem from "@/components/DescriptionItem.vue";
import InputField from "@/components/forms/inputs/InputField.vue";
import SelectInput from "@/components/forms/inputs/SelectInput.vue";
import TextInput from "@/components/forms/inputs/TextInput.vue";
import SortableList from "@/components/SortableList.vue";
import HeadSection from "@/layouts/HeadSection.vue";

interface IngredientErrors {
  amount?: string[];
  amount_max?: string[];
  food?: string[];
  unit?: string[];
  qualifier?: string[];
  optional?: string[];
  note?: string[];
}

interface StepErrors {
  text?: string[];
}

interface IngredientGroupErrors {
  name?: string[];
}

interface FormErrors {
  name?: string[];
  description?: string[];
  servings?: string[];
  ingredients?: IngredientErrors[];
  ingredientGroups?: IngredientGroupErrors[];
  steps?: StepErrors[];
}

const props = defineProps<{
  recipe?: EditableRecipe | null;
  errors: FormErrors | null;
  qualifiers?: Qualifier[];
  foods?: Food[];
  units?: Unit[];
  user: User;
  locale: string;
}>();

const recipeForm = useForm({
  id: props.recipe?.id || null,
  name: props.recipe?.name || "",
  description: props.recipe?.description || "",
  prep_time: props.recipe?.prep_time || "",
  cook_time: props.recipe?.cook_time || "",
  yield_amount: props.recipe?.yield_amount || "",
  servings: props.recipe?.servings || "",
  ingredients: props.recipe?.ingredients || [],
  ingredient_groups: props.recipe?.ingredient_groups || [],
  steps: props.recipe?.steps || [],
});

const { t } = useI18n();
const pageTitle = computed(() =>
  props.recipe ? t("edit.title", { name: props.recipe.name }) : t("recipe.add_new"),
);

const addIngredientGroup = () => {
  recipeForm.ingredient_groups.push({
    id: null,
    order: recipeForm.ingredient_groups.length + 1,
    name: "",
  });
};
const addIngredient = () => {
  recipeForm.ingredients.push({
    id: null,
    order: recipeForm.ingredients.length + 1,
    amount: null,
    amount_max: null,
    food: null,
    unit: null,
    group: null,
    qualifier: null,
    optional: false,
    note: "",
  });
};
const submitRecipeForm = () => {
  recipeForm.post(`${window.location.pathname}${window.location.search}`, {
    only: ["recipe", "ingredients", "ingredientGroups"],
    preserveScroll: true,
    viewTransition: false,
  });
};
const hasErrors = computed((): boolean =>
  recipeForm.errors ? Object.keys(recipeForm.errors).length > 0 : false,
);
</script>

<template>
  <head-section :title="pageTitle" />
  <div class="container mx-auto px-4">
    {{ recipeForm.errors }}
    <form
      class="grid grid-cols-12 gap-4 border-b border-t border-red-500/0"
      :class="hasErrors ? 'border-red-500/100' : ''"
      @submit.prevent="submitRecipeForm"
    >
      <div class="col-span-12">
        <div class="flex flex-wrap sm:flex-nowrap items-center mb-2 md:mb-4">
          <h1
            class="text-2xl pt-2 grow w-full sm:w-auto"
            itemprop="name"
            :style="recipe ? `view-transition-name: recipe-${recipe.slug}-name` : ''"
          >
            {{ pageTitle }}
          </h1>
        </div>
        <breadcrumb-bar
          :current="pageTitle"
          class="p-0"
        />
        <description-item :label="t('edit.name')">
          <input-field
            id="name-field"
            v-model="recipeForm.name"
            :errors="recipeForm.errors?.name"
          />
        </description-item>
        <description-item :label="t('edit.yield')">
          <input-field
            id="yield-field"
            v-model="recipeForm.yield_amount"
            :errors="recipeForm.errors?.yield_amount"
            input-class="w-20"
            placeholder="1"
          />
        </description-item>
        <description-item :label="t('edit.servings')">
          <input-field
            id="servings-field"
            v-model="recipeForm.servings"
            :errors="recipeForm.errors?.servings"
            input-class="w-20"
            placeholder="1"
          />
        </description-item>
        <description-item :label="t('edit.cook_time')">
          <input-field
            id="cook-time-field"
            v-model="recipeForm.cook_time"
            placeholder="00:00:00"
            :errors="recipeForm.errors?.cook_time"
            input-class="w-50"
          />
        </description-item>
        <description-item :label="t('edit.prep_time')">
          <input-field
            id="prep-time-field"
            v-model="recipeForm.prep_time"
            placeholder="00:00:00"
            :errors="recipeForm.errors?.prep_time"
            input-class="w-50"
          />
        </description-item>
        <description-item :label="t('edit.description')">
          <text-input
            id="description-field"
            v-model="recipeForm.description"
            class="max-w-full"
            :errors="recipeForm.errors?.description"
            :placeholder="t('edit.description')"
          />
        </description-item>
        <div class="mt-4">
          <div class="card p-4">
            <div class="card-title pb-2">
              <div class="flex flex-row items-center">
                <h2 class="text-xxl grow w-100 mr-2">{{ t("edit.ingredientGroups") }}</h2>
              </div>
            </div>
            <div class="card-body">
              <div v-if="!recipeForm.ingredient_groups.length">
                {{ t("edit.no_ingredient_groups") }}
              </div>
              <sortable-list v-model="recipeForm.ingredient_groups">
                <template #default="{ item: group }">
                  <div class="flex items-center gap-2">
                    <span class="icon-[tabler--grip-vertical] cursor-move"></span>
                    <input
                      v-model="group.name"
                      class="input grow"
                    />
                  </div>
                </template>
              </sortable-list>
              <button
                type="button"
                class="btn btn-secondary mt-4"
                @click="addIngredientGroup"
              >
                {{ t("edit.add_group") }}
              </button>
            </div>
          </div>
          <div class="card p-4">
            <div class="card-title pb-2">
              <div class="flex flex-row items-center">
                <h2 class="text-xxl grow w-100 mr-2">{{ t("recipe.ingredients") }}</h2>
              </div>
            </div>
            <div class="card-body">
              <div class="flex items-center justify-between gap-2 w-full">
                <div class="w-10">{{ t("edit.order") }}</div>
                <div class="">{{ t("edit.amount") }}</div>
                <div class="">{{ t("edit.food") }}</div>
                <div class="">{{ t("edit.unit") }}</div>
                <div class="">{{ t("edit.qualifier") }}</div>
                <div class="w-12">{{ t("edit.optional") }}</div>
                <div class="">{{ t("edit.notes") }}</div>
              </div>
              <div v-if="!recipeForm.ingredients.length">
                {{ t("edit.no_ingredients") }}
              </div>
              <div v-if="recipeForm.errors?.ingredients">
                {{ recipeForm.errors?.ingredients }}
              </div>
              <sortable-list v-model="recipeForm.ingredients">
                <template #default="{ item: ingredient, index: i }">
                  <div class="flex items-center gap-2 w-full">
                    <div class="flex items-center w-10 cursor-move userselect-none">
                      <span class="icon-[tabler--grip-vertical]"></span>
                    </div>
                    <div class="join">
                      <input-field
                        :id="`ingredient-${i}-amount`"
                        v-model="ingredient.amount"
                        :errors="recipeForm.errors?.ingredients?.[i]?.amount"
                        class="join-item"
                      />
                      <input-field
                        :id="`ingredient-${i}-amount`"
                        v-model="ingredient.amount_max"
                        :errors="recipeForm.errors?.ingredients?.[i]?.amount_max"
                        class="join-item"
                      />
                    </div>
                    <deferred data="foods">
                      <template #fallback>
                        <div>Loading...</div>
                      </template>
                      <select-input
                        v-if="foods"
                        :id="`ingredient-${i}-food`"
                        v-model="ingredient.food"
                        :errors="recipeForm.errors?.ingredients?.[i]?.food"
                        :options="foods"
                        label-key="name"
                      />
                    </deferred>
                    <deferred data="units">
                      <template #fallback>
                        <div>Loading...</div>
                      </template>
                      <select-input
                        v-if="units"
                        :id="`ingredient-${i}-unit`"
                        v-model="ingredient.unit"
                        :errors="recipeForm.errors?.ingredients?.[i]?.unit"
                        :options="units"
                        label-key="name"
                      >
                        <template #option="{ option }">
                          {{ option.name }}
                          <template v-if="option.abbreviation"> ({{ option.abbreviation }})</template>
                        </template>
                      </select-input>
                    </deferred>
                    <deferred data="qualifiers">
                      <template #fallback>
                        <div>Loading...</div>
                      </template>
                      <select-input
                        v-if="qualifiers"
                        :id="`ingredient-${i}-qualifier`"
                        v-model="ingredient.qualifier"
                        :errors="recipeForm.errors?.ingredients?.[i]?.qualifier"
                        :options="qualifiers"
                        label-key="title"
                      />
                    </deferred>
                    <div class="flex items-center gap-1">
                      <input
                        :id="`optional-${i}`"
                        v-model="ingredient.optional"
                        type="checkbox"
                        class="checkbox"
                      />
                      <label
                        class="sr-only"
                        :for="`optional-${i}`"
                      >
                        {{ t("edit.optional") }}
                      </label>
                    </div>
                    <input-field
                      :id="`ingredient-${i}-note`"
                      v-model="ingredient.note"
                      :errors="recipeForm.errors?.ingredients?.[i]?.note"
                    />
                  </div>
                </template>
              </sortable-list>
              <button
                type="button"
                class="btn btn-secondary mt-4"
                @click="addIngredient"
              >
                {{ t("edit.add_ingredient") }}
              </button>
            </div>
          </div>
        </div>
      </div>
      <div class="col-span-12">
        <div v-if="!recipeForm.steps.length">
          {{ t("edit.no_steps") }}
        </div>
        <sortable-list v-model="recipeForm.steps">
          <template #default="{ item: step }">
            <div class="card mb-2 flex flex-row items-center cursor-move">
              <span class="ml-4 icon-[tabler--grip-vertical]"></span>
              <h3 class="card-title p-4">{{ t("recipe.step_title", { step: step.order }) }}</h3>
              <div class="card-body p-4 grow">
                <text-input
                  :id="`step-${step.order}-text`"
                  v-model="step.text"
                  :errors="recipeForm.errors?.steps?.[i]?.text"
                ></text-input>
              </div>
            </div>
          </template>
        </sortable-list>
        <button
          type="button"
          class="btn btn-secondary mt-4"
        >
          {{ t("edit.add_step") }}
        </button>
        <div class="flex justify-end">
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="!recipeForm.isDirty"
          >
            {{ t("edit.save") }}
          </button>
        </div>
      </div>
    </form>
  </div>
</template>
