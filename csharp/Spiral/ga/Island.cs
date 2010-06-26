using System;
using System.Threading;


namespace spiral.ga
{
    public abstract class Island<T>: Pool<T>
    {
        protected Thread thread;

        protected Selection<T> Selection;
        protected Mutation<T> Mutation;
        protected Crossover<T> Crossover;

        #region Current/Best/Worst
        protected T currentGenome;
        protected T bestGenome;
        protected T worstGenome;

        public T CurrentGenome
        {
            get { return currentGenome; }
        }

        public T BestGenome
        {
            get { return bestGenome; }
        }

        public T WorstGenome
        {
            get { return worstGenome; }
        }
        #endregion

        public Island()
            :base()
        {
            thread = new Thread(new ThreadStart(AdvanceEpoch));

            Selection = new Selection<T>();
            Mutation = new Mutation<T>();
            Crossover = new Crossover<T>();
        }

        public virtual void CreateInitial()
        {

        }

        public virtual void AdvanceEpoch()
        {
            PreAdvance();

            PostAdvance();
        }

        public abstract void TestIndividual();

        #region Hooks
        protected virtual void PostAdvance()
        {
        }

        protected virtual void PreAdvance()
        {
        }

        protected virtual void PostTest()
        {

        }

        protected virtual void PreTest()
        {
        }
        #endregion

        public T this[int index]
        {
            get { return base[index]; }
            set
            {
                currentGenome = (T)value;
                base[index] = (T)value;
            }
        }

        public override string ToString()
        {
            return base.ToString();
        }
    }
}
